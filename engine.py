import os
import streamlit as st
from newsapi import NewsApiClient
from openai import OpenAI

client = OpenAI()
openai_api_key = os.getenv("OPENAI_API_KEY")
newsapi = NewsApiClient(api_key='ad3002a4a81a4e6b8c656770d1461042')

# /v2/top-headlines
all_articles = newsapi.get_everything(q='netflix',
                                      language='en',
                                      page_size=5)

st.title('FinTech-GenAI')

relevance_options = ["High", "Medium", "Low"]
sentiment_options = ["High", "Medium", "Low"]
price_prediction_options = ["Up", "Down", "No Idea"]
confidence_options = ["High", "Medium", "Low"]
impact_options = ["Very Bullish", "Bullish",
                  "No Idea", "Bearish", "Very Bearish"]

for article in all_articles['articles']:
    if article['content']:
        article_content = article['content']
        prompt = article_content

        response = client.chat.completions.create(model="gpt-3.5-turbo",
                                                  messages=[{"role": "system",
                                                             "content": "You are a multi-language stock expert that can predict the stock movement, uptrend, downtrend, bullish, bearish of stocks due to its related news."
                                                             "\nThe way you analyze stock movement are following these couple steps:"
                                                             "\n1. Understand the company in all areas such as structure, management, culture, valuation, strengths, weakenss, recent layoffs, recent huge news etc... and compare it to the news/article"
                                                             "\n2. Understand the article relationships with these ares: new announcements, significant investments,product launches,mergers and acquisitions,M&As,legal issues or R&D activities, or any other critical celements that can impact company's growth, value, and ultimately, its stock price."
                                                             "\n3. Recognize the of historical data of the company, maintaining an ongoing narrative. Analyze all recent and crucial company-specific events that could influence stock prices. "
                                                             "\n4. Use your expert opinions, analyze your encompassing in-depth analyses, forecasts, and professional viewpoints on stock performance and market trends after fully analyze the news."
                                                             "\n5. You will provide 2 VERSIONS OF REPORT FOR EACH NEWS!!, first one in ENGLISH and follow by SIMPLIFED CHINESE"
                                                             "\nFinally, you will only write your summary under this format every single time: (You won't answer or say any other words other than this format!)"

                                                             "\nSummary: (Summary of the news/article)."
                                                             "\nRelevance to Keywords; High, Neutral or Low(keyword).(you will only pick one), and you will also conclude the keyword from one of them in here(new announcements, significant investments, product launches,mergers and acquisitions,legal issues or R&D activities, management modification), then replace the 'keyword' in the parenthesis"
                                                             "\nSentiment Level: High, Neutral or Low.(you will only pick one)"
                                                             "\nConfidence level: High, Neutral or Low.(you will only pick one)"
                                                             "\nPrice Movement Prediction: Up, Neutral or Down.(you will only pick one)"
                                                             "\nBase on the information gather above, the impact is: Very Bullish, Bullish, Neutral, Bearish, Very Bearish. (you will only pick one)"
                                                             "\nExpert opinions: (Replace here with the content you wrote on the 4TH STEP!!!)"

                                                             "\n(Here you will write a division line like this, then continue with SIMPLIFIED CHINESE VERSION '--------------------------------以下是中文版本---------------------------------')"

                                                             "\n(below is the format you will use for SIMPLIFIED CHINESE VERSION)"
                                                             "\n文章总结: (提供你文章/新闻的总结)."
                                                             "\n关键词关联度: (高，中立，低(关键词).(你只会选择一个关键词填写)，然后你要从以下关键词中选择一个(公告，关键性投资，新产品发布，并购以及收购，法律，科学研究与试验发展，管理层变更))"
                                                             "\n敏感度: 高，中立，低(你只会选择一个)"
                                                             "\n信心度: 高，中立，低(你只会选择一个)"
                                                             "\n价格走势预测:看涨，中立，看跌(你只会选择一个)"
                                                             "\n根据以上的信息, 此文章/新闻对股价的看法是:非常看涨，看涨，中立，看跌，非常看跌(你只会选择一个)"
                                                             "\n专家看法: (请把上面第四点已经总结的看法移动到这里！！！)"
                                                             },

                                                            {"role": "user",
                                                             "content": prompt
                                                             }])

        report = response.choices[0].message.content

        with st.container():
            st.subheader(article['title'])
            st.write(report)
            st.markdown(f"[Read Article]({article['url']})", unsafe_allow_html=True)

        print(f"Title: {article['title']}")
        for line in report.split('\n'):
            print(line)
        print("------------------------------------------------------------------------------------------------------------")
