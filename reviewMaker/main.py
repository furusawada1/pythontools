from dataclasses import replace
from fileinput import close
import yaml
import jinja2
import datetime
from cerberus import Validator
from pprint import pprint
import pathlib

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
    projectFilename = 'projectData.yml'
    reviewYamlSchemaFilename = 'reviewSchema.yml'

    # フォルダ内に保存されているファイル一覧
    review_list = list(pathlib.Path(base_dir).glob('**/*_reviewData.yml'))

    # jinjaの初期化
    jinja2FsLoader = jinja2.FileSystemLoader(base_dir, encoding='utf-8')
    jinja2Environment = jinja2.Environment(loader=jinja2FsLoader)
    jinja2Environment.filters.update({'replaceBR': lambda content: content.replace('\n', '<br>')})
    jinja2Template = jinja2Environment.get_template('yamlToHtml.html')

    # レビュー議事録を開く
    with open(base_dir + projectFilename, encoding="utf-8") as yamlFile:
        # YAMLをpythonの変数に格納
        yamlData = yaml.safe_load(yamlFile.read())

    # レビュー議事録を開く
    for reviewDataFile in review_list:
        with open(base_dir + reviewDataFile.name, encoding="utf-8") as yamlFile:
            # YAMLをpythonの変数に格納
            reviewData = [obj for obj in yaml.safe_load_all(yamlFile.read())]

            # 集計データを追加
            reviewData = sorted(reviewData, key=lambda x: x['実施日時'])
            yamlData['承認トレース'] = formatCommitDate(yamlData, reviewData)
            yamlData['レビュー集計'] = formatPhaseReviewCnt(yamlData, reviewData)
            yamlData['レビュー'] = reviewData

            with open(base_dir + reviewYamlSchemaFilename, encoding="utf-8") as schemaFile:
                reviewSchema = yaml.safe_load(schemaFile.read())
                reviewValidator = Validator(reviewSchema)
                for data in reviewData:
                    check = reviewValidator.validate(data)
                    if check == False:
                        print("in " + reviewDataFile.name)
                        pprint(reviewValidator.errors)

            # jinja2経由でmarkdownファイルに出力に変換
            htmlData = jinja2Template.render(yamlData)

            # htmlファイルを出力
            with open(base_dir + pathlib.PurePath(reviewDataFile.name).stem + ".html", 'w', newline='', encoding="utf-8") as f:
                f.write(htmlData)
