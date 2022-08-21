from dataclasses import replace
from fileinput import close
import yaml
import jinja2
import datetime
from cerberus import Validator
from pprint import pprint

def formatCommitDate(yaml):
    allFilelist = dict()
    for devPhase in yaml['委託工程']:
        filelist = dict()  # 各工程毎の成果物ファイルの一覧を初期化

        for review in [reviews for reviews in yaml['レビュー'] if (reviews['レビュー工程'] == devPhase)]:
            for file in review['ファイル']:
                # レビュー対象のファイル名を取得
                fileName = file[0]

                # ファイル承認日リスト上にデータがない場合は初期値を設定する
                if not fileName in filelist:
                    filelist.update({fileName: {'dateInner': datetime.date(1970, 1, 1), 'dateOuter': datetime.date(1970, 1, 1)}})

                # 委託先 or 委託元の承認日付を更新する
                commitDate = datetime.datetime.strptime(review['レビュー承認'][1], '%Y-%m-%d').date()
                if ('Tech' in review['レビュー承認'][0]):
                    if (filelist[fileName]['dateInner'] < commitDate):
                        filelist[fileName]['dateInner'] = commitDate
                elif ('ABC' in review['レビュー承認'][0]):
                    if (filelist[fileName]['dateOuter'] < commitDate):
                        filelist[fileName]['dateOuter'] = commitDate

        allFilelist.update({devPhase: filelist})
    return allFilelist


def formatPhaseReviewCnt(yaml):
    allPhaseCnt = dict()

    # 工程毎に集計する
    for devPhase in yaml['委託工程']:
        # レビュー回数を集計
        reviewCnt = len([reviews for reviews in yaml['レビュー']
                        if (reviews['レビュー工程'] == devPhase)])
        indicateCnt = 0
        closeCnt = 0

        # 指摘件数及びClose件数を集計
        for review in [reviews for reviews in yaml['レビュー'] if (reviews['レビュー工程'] == devPhase)]:
            if review['指摘事項']:
                indicateCnt += len([indicate for indicate in review['指摘事項'] if indicate['対策'][2] in ['指摘', '誤記']])
                closeCnt += len([indicate for indicate in review['指摘事項'] if indicate['状況'] == 'Close'])

        # 工程名称をキーにして集計結果を保持   
        allPhaseCnt.update(
            {devPhase: {'レビュー回数': reviewCnt, '指摘件数': indicateCnt, 'クローズ件数': closeCnt, '未クローズ件数': indicateCnt - closeCnt}})

    return allPhaseCnt


if __name__ == "__main__":
    base_dir = './'
    reviewName = 'xxx_reviewData'
    jinjaFilename = 'yamlToHtml.html'
    reviewYamlFilename = reviewName + '.yml'
    reviewYamlSchemaFilename = 'reviewSchema.yml'

    # jinjaの初期化
    jinja2FsLoader = jinja2.FileSystemLoader(base_dir, encoding='utf-8')
    jinja2Environment = jinja2.Environment(loader=jinja2FsLoader)
    jinja2Template = jinja2Environment.get_template(jinjaFilename)

    # レビュー議事録を開く
    with open(base_dir + reviewYamlFilename, encoding="utf-8") as yamlFile:
        # YAMLをpythonの変数に格納
        yamlData = yaml.safe_load(yamlFile.read())

        # 集計データを追加
        yamlData['承認トレース'] = formatCommitDate(yamlData)
        yamlData['レビュー集計'] = formatPhaseReviewCnt(yamlData)

        with open(base_dir + reviewYamlSchemaFilename, encoding="utf-8") as schemaFile:
            reviewSchema = yaml.safe_load(schemaFile.read())
            reviewValidator = Validator()
            check = reviewValidator.validate(yamlData, reviewSchema)
            if check == False:
                pprint(reviewValidator.errors)

        # jinja2経由でmarkdownファイルに出力に変換
        htmlData = jinja2Template.render(yamlData)

        # htmlファイルを出力
        with open(base_dir + reviewName + ".html", 'w', newline='', encoding="utf-8") as f:
            f.write(htmlData)
