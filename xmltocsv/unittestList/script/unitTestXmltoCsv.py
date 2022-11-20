import csv
from xml.etree import ElementTree
import re
import glob
import os
import subprocess

def xml2csv(path):
    unitTestList = {}

    # 単体テストシーケンスの.cファイルの解析
    xmlFiles = glob.glob(f'{path}/build/doxygen/xml/Test*.xml')
    print(f'analyze {path}/build/doxygen/xml/Test*.xml')
    for xmlFile in xmlFiles:
        tree = ElementTree.parse(xmlFile)
        root = tree.getroot()
        funcname = ""

        filename = root.find("./compounddef/compoundname").text
        for memberdef in root.findall("./compounddef/sectiondef[@kind='func']/memberdef[@kind='function']"):

            brief = None
            detailed = None
            testPre=""
            testSeq=""
            testPost=""

            funcname = memberdef.find("./name").text
            if funcname == None:
                continue
            # print(funcname)

            briefdescription = memberdef.find("briefdescription/para")
            if briefdescription != None:
                brief = re.sub('\\n','\r\n', briefdescription.text)
            else:
                brief = "なし"
            # print(brief)

            detaileddescription = memberdef.find("detaileddescription/para") 
            if detaileddescription != None:
                detailed = re.sub('\\n','\r\n', detaileddescription.text)
            else:
                detailed = "なし"
            # print(detailed)

            verbatim = memberdef.findall('inbodydescription/para/verbatim')
            for testParam in verbatim:
                tempParam = testParam.text
                tempParam = re.sub('^(事前条件|テストシーケンス|チェックポイント)\s*\n','', tempParam)
                tempParam = re.sub('^///\s*\n','', tempParam)
                tempParam = re.sub('///[ ]*$','', tempParam)
                tempParam = re.sub('\\n','\r\n', tempParam)

                if testParam.text.startswith('事前条件'):
                    testPre = tempParam
                elif testParam.text.startswith('テストシーケンス'):
                    testSeq = tempParam
                elif testParam.text.startswith('チェックポイント'):
                    testPost = tempParam
    
            unitTestList.update({funcname:{"ファイル名":filename, "テストケース名":funcname, "大項目":brief, "小項目":detailed, "事前条件":testPre, "テストシーケンス":testSeq, "チェックポイント":testPost}})

    # 単体テストの結果ファイルの解析
    reportFiles = glob.glob(f'{path}/build/artifacts/test/report.xml')
    print(f'analyze {path}/build/artifacts/test/report.xml')
    for reportFile in reportFiles:
        tree = ElementTree.parse(reportFile)
        root = tree.getroot()
        funcname = ""

        for name in root.findall("./SuccessfulTests/Test/Name"):
            unitTestList[re.sub('.+::','', name.text)].update({"結果":"SUCESS"})

        for name in root.findall("./FailedTests/Test/Name"):
            unitTestList[re.sub('.+::','', name.text)].update({"結果":"FAIL"})

        for name in root.findall("./IgnoredTests/Test/Name"):
            unitTestList[re.sub('.+::','', name.text)].update({"結果":"PASS"})

    # csv書き込み
    print(f"output csv file: {path}/build/unitTestList/testlist.csv")
    with open(f'{path}/build/unitTestList/testlist.csv', 'w', encoding='shift_jis') as f:
        writer = csv.DictWriter(f, ["ファイル名", "テストケース名", "大項目","小項目","事前条件","テストシーケンス","チェックポイント","結果"])
        writer.writeheader()
        for key,val in unitTestList.items():
            writer.writerow(val)

if __name__ == '__main__':
    currentDir = os.getcwd()

    # 出力先フォルダ作成
    if not os.path.isdir(f'{currentDir}/build/unitTestList'):
        print(f'mkdir -p {currentDir}/build/unitTestList')
        os.makedirs(f'{currentDir}/build/unitTestList')

    # Doxygen経由で関数リストxml出力
    print(f'execute doxygen  {currentDir}/unittestList/script/Doxyfile')
    subprocess.run(['doxygen', f'{currentDir}/unittestList/script/Doxyfile'])

    # xmlから単体テストリスト(csv)出力
    print(f'create unit testlist')
    xml2csv(currentDir)
