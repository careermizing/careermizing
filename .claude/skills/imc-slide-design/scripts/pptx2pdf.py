"""
PPTX → PDF (LibreOffice UNO) — 한글·영문 사이 자동 간격(Asian autospace)을 끄고 내보낸다.

LibreOffice는 기본적으로 한글과 숫자·영문 사이에 간격을 넣는다("1.5 억").
그래서 미리보기가 PowerPoint와 다르게 보이고 폭 점검도 틀어진다. 이 스크립트는 모든 텍스트 문단(표 셀 포함)의
ParaIsCharacterDistance를 False로 바꾼 다음 PDF로 내보낸다.

    python3 pptx2pdf.py in.pptx out.pdf
"""
import os
import subprocess
import sys
import time

import uno
from com.sun.star.beans import PropertyValue


def _pv(name, value):
    p = PropertyValue()
    p.Name, p.Value = name, value
    return p


def _fix_text(obj):
    try:
        txt = obj.getText() if hasattr(obj, "getText") else obj
        enum = txt.createEnumeration()
    except Exception:
        try:
            enum = obj.createEnumeration()   # 표 셀은 자체가 XText
        except Exception:
            return
    while enum.hasMoreElements():
        para = enum.nextElement()
        try:
            para.ParaIsCharacterDistance = False
        except Exception:
            pass


def _walk(shapes):
    for i in range(shapes.getCount()):
        sh = shapes.getByIndex(i)
        if sh.supportsService("com.sun.star.drawing.GroupShape"):
            _walk(sh)
            continue
        if "TableShape" in sh.ShapeType:
            model = sh.Model
            for r in range(model.Rows.getCount()):
                for c in range(model.Columns.getCount()):
                    cell = model.getCellByPosition(c, r)
                    try:  # 표 셀은 문단 열거가 안 되므로 셀 속성으로 지정
                        cell.setPropertyValue("ParaIsCharacterDistance", False)
                    except Exception:
                        _fix_text(cell)
            continue
        if hasattr(sh, "getText"):
            _fix_text(sh)


def main(src, dst):
    port = 2002 + os.getpid() % 1000
    proc = subprocess.Popen(
        ["soffice", "--headless", "--invisible", "--norestore", "--nologo",
         f"-env:UserInstallation=file:///tmp/lo_cm_{port}",
         f"--accept=socket,host=127.0.0.1,port={port};urp;"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        local = uno.getComponentContext()
        resolver = local.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local)
        ctx = None
        for _ in range(60):
            try:
                ctx = resolver.resolve(
                    f"uno:socket,host=127.0.0.1,port={port};urp;StarOffice.ComponentContext")
                break
            except Exception:
                time.sleep(0.5)
        if ctx is None:
            raise RuntimeError("LibreOffice 연결 실패")
        desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(os.path.abspath(src)),
                                           "_blank", 0, (_pv("Hidden", True),))
        pages = doc.getDrawPages()
        for i in range(pages.getCount()):
            _walk(pages.getByIndex(i))
        doc.storeToURL(uno.systemPathToFileUrl(os.path.abspath(dst)),
                       (_pv("FilterName", "impress_pdf_Export"),))
        doc.close(True)
        try:
            desktop.terminate()
        except Exception:
            pass
    finally:
        time.sleep(0.5)
        proc.kill()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
