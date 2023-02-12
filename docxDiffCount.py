from os import getcwd, path, remove
from sys import stderr
from win32com import client
import time
from docx import Document
import argparse

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML


WORD_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TEXT = WORD_NAMESPACE + "t"
DELTEXT = WORD_NAMESPACE + "delText"

def cmp(originalFileName, modifyFileName):
    ''' docxを比較する '''
    currentDir = getcwd() + '\\'
    cmp_file = currentDir + '_cmp_.docx'
    if path.exists(cmp_file):
        remove(cmp_file)

    # 差分docxファイル生成
    app = client.gencache.EnsureDispatch("Word.Application")
    openFileNew = app.CompareDocuments(app.Documents.Open(originalFileName),
                                       app.Documents.Open(modifyFileName),
                                       Destination=2,
                                       Granularity=1,
                                       IgnoreAllComparisonWarnings=True)
    openFileNew.PageSetup.PaperSize = 7 # A4
    openFileNew.SaveAs2(cmp_file, FileFormat=16, CompatibilityMode=15)
    openFileNew.Close()

    # w:lastrenderedpagebreakタグの設定(wordにpage breakの設定を促してみる)
    openFileNew2 = app.Documents.Open(cmp_file)
    selection = app.Selection
    selection.InsertBreak(7)
    time.sleep(5) # sleepしないと「w:lastrenderedpagebreak」が設定されない
    openFileNew2.SaveAs2(cmp_file, FileFormat=12, CompatibilityMode=15)
    openFileNew2.Close()

    app.Quit(SaveChanges=0)
    print('[output] compare file: '+cmp_file)
    return cmp_file

def checkModify(p, pn):
    ''' 削除、挿入を判定する '''
    xml = p._p.xml
    ret = False
    if "<w:del " in xml:
        xmlTree = XML(xml)
        texts = (node.text for node in xmlTree.iter(DELTEXT))
        print("PageNum:" + str(pn) + " delete ", "".join(texts))
        ret = True

    if "<w:ins " in xml:
        xmlTree = XML(xml)
        texts = (node.text for node in xmlTree.iter(TEXT))
        print("PageNum:" + str(pn) + " insert ", "".join(texts))
        ret = True

    return ret


def checkPageBreak(p):
    ''' ページ端をカウントする '''
    if "w:lastRenderedPageBreak" in p._p.xml:
        return 1
    return 0

def main():
    # get arg
    dir = getcwd() + '\\'
    argParser = argparse.ArgumentParser(description='docx diff conut')
    argParser.add_argument('--originalfile', default=dir+"document_#2.docx", help='original file name')
    argParser.add_argument('--revisedfile', default=dir+"document_#4.docx", help='revised file name')

    args = argParser.parse_args()
    originalFileName = args.originalfile
    revisedFileName = args.revisedfile

    # create Compare docx
    print("[input] original file: " + originalFileName, file=stderr)
    print("[input] revised file: " + revisedFileName, file=stderr)
    compareFileName = cmp(originalFileName, revisedFileName)

    # count diff page
    doc = Document(compareFileName)
    modifyPageList = []
 
    pn = 0
    for p in doc.paragraphs:
        pn += checkPageBreak(p)
        if checkModify(p, pn):
            modifyPageList.append(pn)

    # print result
    print(set(modifyPageList))
    print(len(set(modifyPageList)))

if __name__ == '__main__':
    main()

