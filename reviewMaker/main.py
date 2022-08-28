from dataclasses import replace
from fileinput import close
import yaml
import jinja2
import datetime
from cerberus import Validator
from pprint import pprint


def formatCommitDate(baseData, yamlData):
    allFilelist = dict()
    for devPhase in baseData['委託工程']:
        filelist = dict()  # 各工程毎の成果物ファイルの一覧を初期化
        for review in [reviews for reviews in yamlData if (reviews['工程'] == devPhase)]:
            for type, files in review['ファイル'].items():
                for file in files:
                    fileName = file[0]  # レビュー対象のファイル名を取得

                    # ファイル承認日リスト上にデータがない場合は初期値を設定する
                    if not fileName in filelist:
                        filelist.update({fileName: {'dateInner': datetime.date(
                            1970, 1, 1), 'dateOuter': datetime.date(1970, 1, 1)}})

                    # 委託先 or 委託元の承認日付を更新する
                    commitDate = datetime.datetime.strptime(
                        review['レビュー承認者_承認日'][1], '%Y-%m-%d').date()
                    if ('Tech' in review['レビュー承認者_承認日'][0]):
                        if (filelist[fileName]['dateInner'] < commitDate):
                            filelist[fileName]['dateInner'] = commitDate
                    elif ('ABC' in review['レビュー承認者_承認日'][0]):
                        if (filelist[fileName]['dateOuter'] < commitDate):
                            filelist[fileName]['dateOuter'] = commitDate

        allFilelist.update({devPhase: filelist})
    return allFilelist


def formatPhaseReviewCnt(baseData, yamlData):
    allPhaseCnt = dict()

    # 工程毎に集計する
    for devPhase in baseData['委託工程']:
        # レビュー回数を集計
        reviews = [reviews for reviews in yamlData if (
            reviews['工程'] == devPhase)]
        reviewCnt = len(reviews)
        indicateCnt = 0
        closeCnt = 0

        # 指摘件数及びClose件数を集計
        for review in reviews:
            if review['指摘'] != [None]:
                indicateCnt += len([indicate for indicate in review['指摘']
                                   if len(indicate) == 5 and indicate[4] in ['指摘', '誤記']])
                closeCnt += len([indicate for indicate in review['指摘']
                                if len(indicate) == 5 and indicate[3] != None])

        # 工程名称をキーにして集計結果を保持
        allPhaseCnt.update(
            {devPhase: {'レビュー回数': reviewCnt, '指摘件数': indicateCnt, 'クローズ件数': closeCnt, '未クローズ件数': indicateCnt - closeCnt}})

    return allPhaseCnt

if __name__ == "__main__":
    base_dir = './reviewMaker/'
    baseName = 'baseData.yml'
    reviewName = 'reviewData'
    jinjaFilename = 'yamlToHtml.html'
    reviewYamlFilename = reviewName + '.yml'
    reviewYamlSchemaFilename = 'reviewSchema.yml'

    # jinjaの初期化
    jinja2FsLoader = jinja2.FileSystemLoader(base_dir, encoding='utf-8')
    jinja2Environment = jinja2.Environment(loader=jinja2FsLoader)
    jinja2Environment.filters.update({'replaceBR': lambda content: content.replace('\n', '<br>')})
    jinja2Template = jinja2Environment.get_template(jinjaFilename)

    # レビュー議事録を開く
    with open(base_dir + baseName, encoding="utf-8") as yamlFile:
        # YAMLをpythonの変数に格納
        baseData = yaml.safe_load(yamlFile.read())

    # レビュー議事録を開く
    with open(base_dir + reviewYamlFilename, encoding="utf-8") as yamlFile:
        # YAMLをpythonの変数に格納
        yamlData = [obj for obj in yaml.safe_load_all(yamlFile.read())]

        # 集計データを追加
        yamlData = sorted(yamlData, key=lambda x: x['実施日時(YYYY-M-D hh:mm:ss)'])
        baseData['承認トレース'] = formatCommitDate(baseData, yamlData)
        baseData['レビュー集計'] = formatPhaseReviewCnt(baseData, yamlData)
        baseData['レビュー'] = yamlData

#        with open(base_dir + reviewYamlSchemaFilename, encoding="utf-8") as schemaFile:
#            reviewSchema = yaml.safe_load(schemaFile.read())
#            reviewValidator = Validator()
#            check = reviewValidator.validate(yamlData, reviewSchema)
#            if check == False:
#                pprint(reviewValidator.errors)

        # jinja2経由でmarkdownファイルに出力に変換
        htmlData = jinja2Template.render(baseData)

        # htmlファイルを出力
        with open(base_dir + reviewName + ".html", 'w', newline='', encoding="utf-8") as f:
            f.write(htmlData)
