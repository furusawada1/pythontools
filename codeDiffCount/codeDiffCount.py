import subprocess
import pprint
import os
import yaml
import re
import pprint

def cmpCode(gitBase, reposUrl, rev1,rev2):

    # gitリポジトリの最新版の取得
    repoBase = gitBase + os.path.splitext(os.path.basename(reposUrl))[0]
    if(not os.path.exists(repoBase)):
        subprocess.check_output(['git', 'clone',reposUrl],  cwd=gitBase)
    else:
        subprocess.check_output(['git', 'rebase'], cwd=repoBase)

    # clocの実行
    yamlByte = subprocess.check_output(['cloc-1.94.exe',
                                    '--by-file', '--git', '--diff', rev1, rev2,'--yaml','--quiet'], cwd=repoBase)

    # 実行結果(yaml)の整形及び変数への代入
    yamString = yamlByte.decode().replace('\r', '')     # 改行コードの変更
    yamString = re.sub(r'^.+---', r'---', yamString, flags=re.DOTALL) # ---より前の出力を削除
    yamlData = yaml.safe_load(yamString)

    # ファイル毎に集計し直す
    clocDict = {}
    for key in ['added', 'removed', "modified", "same"]:
        for filenameFull, value in yamlData[key].items():
            pathLength = len(os.environ['TEMP']) + 11 # clocで--git --diffを行う際のパスの不要部分の長さ(ex. x:\temp\xxxxxxxxxx)
            filename = filenameFull[pathLength:] # パスの不要部分を削除
            clocDict.setdefault(filename, {"added": 0, "removed": 0, "modified":0, "same":0})
            clocDict[filename] |= {key: value['code']}

    for key, value in clocDict.items():
        added = clocDict[key]['added']
        modified = clocDict[key]['modified']
        removed = clocDict[key]['removed']
        same = clocDict[key]['same']

        if added == 0 and modified == 0:
            # removed != 0
            if same == 0:
                #一致する箇所がない＝ファイル削除
                clocDict[key]['type'] = "削除"
            else:
                #一致する箇所がある＝ファイル一部削除
                clocDict[key]['type'] = "修正箇所"
        elif (added != 0 or modified != 0) and same == 0:
            # 一致する箇所がない＝新規作成or全部修正
            clocDict[key]['type'] = "全部"
        else:
            # 一致する箇所がある＝一部修正
            clocDict[key]['type'] = "修正箇所"

    pprint.pprint(clocDict)
#    csvByte = subprocess.check_output(['D:\\pythontools\\pythontools\\cloc-1.94.exe',
#                                    '--by-file', '--git', '--diff', rev1, rev2,'--csv','--quiet'], cwd=repoBase)
#    print(csvByte.decode())

if __name__ == '__main__':
    dir = os.path.dirname(os.path.abspath(__file__)) + '\\temp\\'
    cmpCode(dir, 'https://gitlab.com/isola/pythontools.git','688f52b1','e2c3dbc6')
