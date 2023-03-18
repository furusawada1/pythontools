ChatGPTの紹介

プログラマーにもChatGPTが必要？！年収2400万円の実力を手軽に手に入れよう！

Q
chatgptは年収2400万円のプログラミングエンジニア相当の実力があると言うニュースが最近ありました。素晴らしいと思います。chat GPTをエンジニアに使用してもらえるように紹介するキャッチーな記事のタイトルを考えてもらっていいですか？

ChatGPTとは

ChatGPTは、オープンAIが開発した自然言語処理技術を用いた言語モデルです。
この技術を応用することで、ChatGPTは人工知能による自然な会話を可能にし、言語に関する様々なタスクに対応できるようになりました。

最近のニュースでは、ChatGPTが年収2400万円のプログラミングエンジニア相当の実力を持つという報道がありました。
ChatGPTは、プログラマーのようにロジックやアルゴリズムを書く必要がなく、自然な言葉でタスクを伝えるだけで、プログラマー以上の実力を発揮することができます。

- Google is asking employees to test potential ChatGPT competitors, including a chatbot called ‘Apprentice Bard’
  https://www.cnbc.com/2023/01/31/google-testing-chatgpt-like-chatbot-apprentice-bard-with-employees.html
- ChatGPTがGoogleのコーディング職の試験を受けると年収2400万円のレベル3エンジニアとして合格する
  https://gigazine.net/news/20230206-chatgpt-passed-google-coding-interview/

Q
chatgptは年収2400万円のプログラミングエンジニア相当の実力があると言うニュースが最近ありました。紹介をお願いできますか？

言いたいこと

・この1~2年位にAIの技術が恐ろしいレベルで進化しています。
・今回触りを紹介しますので、とにかく皆さんに試してみて欲しいです。
・現状のAI技術でできること、できないことが分かってくると思います。
・そこをスタート地点として業務への適用を一緒に考えていきたいです。

個人の感想です

キーワードの整理

- OpenAIは、人工知能に関する研究や開発を行うAI研究機関
- OpenAIが開発したGPT(Generative Pre-trained Transformer)は、自然言語処理技術を用いて文章を生成するAI
  - 2020年7月にOpenAIがGPT-3が発表、2022年頃からGPT-3を利用した各種サービスが話題になった
  - MicrosoftがOpenAIに対して出資やパートナー契約を締結
- GPTを利用した各種サービス
  - GitHub Copilot: GPT-3を使用したコーディング支援
  - OpenAI ChatGPT: GPT-3.5を使用したチャットボット
  - Microsoft Bing: GPT-4を使用したAI検索
  - 等々

ChatGPTを試してみる

プログラマなので関数を作らせてみました。

raw画像を入力とし、画素のR、G、B成分を個別のバッファに分解して出力する関数を作成してください。
入力画像、出力画像はそれぞれ１画素uint32_tの型の一次元配列のポインタとして引数に与えられます。
１画素はR,G,Bの輝度をそれぞれ8bitで持ちます。
残りの8bitは透過率を意味しますが今回は無視してください。
他の引数として入力画像の幅高を指定します。
入力画像を保持するバッファは画像1ライン毎に32byteのアラインの制約があり、画像の幅がアラインに合わない場合、有効な画素が設定されていない部分はスキップする対応が必要になります。

```
void decomposeRGB(uint32_t* inputImage, uint8_t* redBuffer, uint8_t* greenBuffer, uint8_t* blueBuffer, int width, int height) {
    int inputPitch = width + (32 - width % 32) % 32; // 画像の幅にアラインするためのピッチ
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            uint32_t pixel = inputImage[y * inputPitch + x]; // 画像のx,y座標に対応するピクセルを取得
            redBuffer[y * width + x] = (pixel >> 16) & 0xff; // R成分を取り出して、redBufferに格納
            greenBuffer[y * width + x] = (pixel >> 8) & 0xff; // G成分を取り出して、greenBufferに格納
            blueBuffer[y * width + x] = pixel & 0xff; // B成分を取り出して、blueBufferに格納
        }
    }
}
```

前述の仕様に加え、出力画像の解像度を四分の一にして下さい。その際、画素値を平均するなどの計算は不要で幅、高それぞれの読み込みをスキップするだけで良いです。

```
void decomposeRGBandDownsample(uint32_t* inputImage, uint8_t* redBuffer, uint8_t* greenBuffer, uint8_t* blueBuffer, int width, int height) {
    int inputPitch = width + (32 - width % 32) % 32; // 画像の幅にアラインするためのピッチ
    int outputWidth = width / 4;
    int outputHeight = height / 4;
    for (int y = 0; y < outputHeight; ++y) {
        for (int x = 0; x < outputWidth; ++x) {
            uint32_t pixel = inputImage[(y * 4) * inputPitch + (x * 4)]; // 4x4のブロックの左上の画素を取得
            redBuffer[y * outputWidth + x] = (pixel >> 16) & 0xff; // R成分を取り出して、redBufferに格納
            greenBuffer[y * outputWidth + x] = (pixel >> 8) & 0xff; // G成分を取り出して、greenBufferに格納
            blueBuffer[y * outputWidth + x] = pixel & 0xff; // B成分を取り出して、blueBufferに格納
        }
    }
}
```

関数にdoxygen形式のコメントを付与してください。

```
/**
 * @brief raw画像を入力とし、画素のR、G、B成分を個別のバッファに分解して、出力画像の解像度を四分の一にする関数
 *
 * @param inputImage 入力画像を表すuint32_t型の配列
 * @param redBuffer R成分を格納するuint8_t型の配列
 * @param greenBuffer G成分を格納するuint8_t型の配列
 * @param blueBuffer B成分を格納するuint8_t型の配列
 * @param width 入力画像の幅
 * @param height 入力画像の高さ
 */
void decomposeRGBandDownsample(uint32_t* inputImage, uint8_t* redBuffer, uint8_t* greenBuffer, uint8_t* blueBuffer, int width, int height) {
(略)
}
```

関数に引数チェック処理を追加してください。
```
(略)
void decomposeRGBandDownsample(uint32_t* inputImage, uint8_t* redBuffer, uint8_t* greenBuffer, uint8_t* blueBuffer, int width, int height) {
    if (inputImage == NULL || redBuffer == NULL || greenBuffer == NULL || blueBuffer == NULL || width <= 0 || height <= 0) {
        // 引数が不正な場合は、処理を中止する
        return;
    }
(略)
}
```

この関数の単体テストを作成してください。テストフレームワークはceedlingを使用してください。

```
#include "unity.h"
#include "decompose_rgb.h"

void test_decomposeRGBandDownsample() {
    // テストデータの用意
    uint32_t inputImage[16] = {
        0xff0000ff, 0xff00ffff, 0xff0000ff, 0xff00ffff,
        0xff00ff00, 0xff00ff00, 0xff00ff00, 0xff00ff00,
        0xffff0000, 0xffff0000, 0xffff0000, 0xffff0000,
        0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff
    };
    uint8_t redBuffer[4];
    uint8_t greenBuffer[4];
    uint8_t blueBuffer[4];

    // 関数の呼び出し
    decomposeRGBandDownsample(inputImage, redBuffer, greenBuffer, blueBuffer, 4, 4);

    // 期待値の用意
    uint8_t expectedRedBuffer[4] = {0xff, 0x00, 0xff, 0xff};
    uint8_t expectedGreenBuffer[4] = {0x00, 0xff, 0x00, 0xff};
    uint8_t expectedBlueBuffer[4] = {0xff, 0x00, 0xff, 0xff};

    // 結果の確認
    TEST_ASSERT_EQUAL_MEMORY(expectedRedBuffer, redBuffer, sizeof(expectedRedBuffer));
    TEST_ASSERT_EQUAL_MEMORY(expectedGreenBuffer, greenBuffer, sizeof(expectedGreenBuffer));
    TEST_ASSERT_EQUAL_MEMORY(expectedBlueBuffer, blueBuffer, sizeof(expectedBlueBuffer));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_decomposeRGBandDownsample);
    return UNITY_END();
}
```

この関数の仕様書を作成してください。

```
関数名: decomposeRGBandDownsample

機能: 入力されたraw画像を解析し、画素のR、G、B成分を個別のバッファに分解し、出力画像の解像度を四分の一にする

プロトタイプ: void decomposeRGBandDownsample(uint32_t* inputImage, uint8_t* redBuffer, uint8_t* greenBuffer, uint8_t* blueBuffer, int width, int height)

引数:

inputImage: raw画像を表すuint32_t型の配列
redBuffer: R成分を格納するuint8_t型の配列
greenBuffer: G成分を格納するuint8_t型の配列
blueBuffer: B成分を格納するuint8_t型の配列
width: 入力画像の幅
height: 入力画像の高さ

戻り値: なし

仕様:

入力画像を表すuint32_t型の配列から、画素のR、G、B成分を個別のuint8_t型のバッファに分解する
出力画像の幅と高さは、入力画像の幅と高さをそれぞれ4で割った値となる
出力画像の解像度を四分の一にするため、幅と高さそれぞれについて、4ピクセル毎に1ピクセルを出力する
画素値の平均を計算することはなく、単純に4ピクセル毎に1ピクセルを読み込み、それを出力画像に書き込む
有効な画素が設定されていない部分はスキップされる
入力画像の幅にアラインするためのピッチは、32byteのアラインの制約に従って計算される
引数が不正な場合は、処理を中止する

注意事項:

入力画像、出力画像のバッファはそれぞれ1ライン毎に32byteのアラインメント制約がある
この関数は、入力画像を書き換えることはない
```

ChatGPTができること
・要求仕様に基づく設計書作成
・設計書の文面のレビュー
・仕様に基づく実装、テスト作成
・

利用する上で気を付けること

Q. chatGPTで生成したソースコードや文章を業務に活用する上で、ライセンス上で気をつける必要はありますか？

ChatGPTで生成したソースコードや文章を業務に活用する際には、ライセンス上の注意が必要です。

OpenAIが提供するChatGPTは、生成されたコンテンツに対してライセンスを定めています。
商用利用や再配布を含む利用については、OpenAIとの商用ライセンス契約を結ぶ必要があります。
一方、個人利用や非商用利用については、オープンソースライセンスに従って利用することができます。

ソースコードや文章を利用する前に、利用規約や契約内容をよく確認し、ライセンス上の義務を遵守するようにしてください。
不正な利用が発覚した場合には、法的責任が生じる可能性があるため、注意が必要です。

現在の

以前のChatGPTの規約では商用利用に

https://openai.com/terms/

https://note.com/tomotana/n/n4a3799b4ec66

最後に

- 最近のAI技術は超すごい。産業革命レベル。
- データの取り扱いには気をつける必要があり、利用者側でリスク対策が必要
  - AIが間違った回答を返すリスク
  - ライセンス上のリスク
  - 外部サービスに機密情報をを渡すことのリスク
- ただし、今後AIの進化は止まらないと思われるので、業務へのAI技術の活用を検討して、
  生産性を向上させる必要がある
  

以上
