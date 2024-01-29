import os
from dotenv import load_dotenv
import streamlit as st
from newsapi import NewsApiClient
from openai import OpenAI
#import datetime
import time

load_dotenv()
client = OpenAI()
openai_api_key = os.getenv("OPENAI_API_KEY")
newsapi = NewsApiClient(api_key='ad3002a4a81a4e6b8c656770d1461042')

custom_css = """
<style>
.big-font {
    font-size:300%;
    text-align: center;
    margin: 10px 0px;
    color: black;
    text-shadow: 2px 2px #CCCCCC;
}

.typing-container {
    text-align: center;
    width: 100%;
}

.typing-animation {
    display: inline-block;
    font-size:150%;
    color: black;
    white-space: nowrap;
    overflow: hidden;
    border-right: .15em solid black;
    animation: typing 3s steps(40, end), blink-caret 1s step-end infinite;
}

@keyframes typing {
    from { width: 0 }
    to { width: 50% }
}

@keyframes blink-caret {
    50% { border-color: transparent }
}

.small-font {
    font-size:150%;
    text-align: center;
    color: black;
    margin-bottom: 30px;
}

.news-container {
    background-color: #f0f2f6;  
    border: 1px solid #e1e4e8;  
    border-radius: 10px;        
    padding: 10px;              
    margin-bottom: 10px;        
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown('<p class="big-font">NewsAI</p>', unsafe_allow_html=True)
st.markdown('<div class="typing-container"><p class="typing-animation">Find Anything, With Something</p></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 2, 1]) 

with col1:
    user_input = st.text_input("What you want to discover today?", "")

with col2:
    category_option = st.selectbox(
    "Category",
    ("General", "Business", "Entertainment", "Health", "Science", "Sports", "Technology"),
    index=0 
    )

with col3:
     country_option = st.selectbox(
          "Country",
          ("ae", "ar", "at", "au", "be",
           "bg", "br", "ca", "ch", "cn", 
           "co", "cu", "cz", "de", "eg",
           "fr", "gb", "gr", "hk", "hu",
           "id", "ie", "il", "in", "it",
           "jp", "kr", "lt", "lv", "ma",
           "mx", "my", "ng", "nl", "no", 
           "nz", "ph", "pl", "pt", "ro",
           "rs", "ru", "sa", "se", "sg",
           "si", "sk", "th", "tr", "tw",
           "ua", "us", "ve", "za")
     )

#def calculate_from_date(time_frame):
    #now = datetime.datetime.now()
    #if time_frame == "1D":
        #return now - datetime.timedelta(days=1)
    #elif time_frame == "3D":
        #return now - datetime.timedelta(days=3)
    #elif time_frame == "1W":
        #return now - datetime.timedelta(days=7)
    #elif time_frame == "1M":
        #return now - datetime.timedelta(days=30)
    #return now

#def format_datetime(dt):
    #return dt.strftime('%Y-%m-%dT%H:%M:%S')

if st.button('Search'):
    placeholder = st.empty()
    #from_date = calculate_from_date(time_frame)
    #to_date = datetime.datetime.now()
    #formatted_from_date = format_datetime(from_date)
    #formatted_to_date = format_datetime(to_date)
    for _ in range(10):  
        for dot_count in range(4):
            loading_text = f"Searching the best news of {user_input} for you right now{'.' * dot_count}"
            placeholder.info(loading_text)
            time.sleep(0.5)

    all_articles = newsapi.get_top_headlines(q=user_input,
                                          category=category_option.lower(),
                                          language='en',
                                          country=country_option)

    #all_articles = newsapi.get_everything(q=company_name,
                                            #from_param=formatted_from_date,
                                            #to=formatted_to_date,
                                            #language='en',
                                            #page_size=5)
    placeholder.empty()

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
                                                                    "(you need to make a seperate line for for '\n'!!!!)"

                                                                    "\n(Here you will write a division line like this, then continue with SIMPLIFIED CHINESE VERSION '--------------------------------以下是中文版本---------------------------------')"

                                                                    "\n(below is the format you will use for SIMPLIFIED CHINESE VERSION)"
                                                                    "\n文章总结: (提供你文章/新闻的总结)."
                                                                    "\n关键词关联度: (高，中立，低(关键词).(你只会选择一个关键词填写)，然后你要从以下关键词中选择一个(公告，关键性投资，新产品发布，并购以及收购，法律，科学研究与试验发展，管理层变更))"
                                                                    "\n敏感度: 高，中立，低(你只会选择一个)"
                                                                    "\n信心度: 高，中立，低(你只会选择一个)"
                                                                    "\n价格走势预测:看涨，中立，看跌(你只会选择一个)"
                                                                    "\n根据以上的信息, 此文章/新闻对股价的看法是:非常看涨，看涨，中立，看跌，非常看跌(你只会选择一个)"
                                                                    "\n专家看法: (请把上面第四点已经总结的看法移动到这里！！！)"
                                                                    "(you need to make a seperate line for for '\n'!!!!)"
                                                                    },

                                                                    {"role": "user",
                                                                    "content": prompt
                                                                    }])

                report = response.choices[0].message.content

                article_html = f"""
                <div style='background-color: #f0f2f6; border: 1px solid #e1e4e8; border-radius: 10px; padding: 10px; margin-bottom: 10px;'>
                    <h2>{article['title']}</h2>
                    <p>{report}</p>
                    <a href="{article['url']}" target="_blank" style='background-color: #4CAF50; border: none; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 5px; box-shadow: 0 5px #999;'>Read Article</a>
                </div>
                """
                st.markdown(article_html, unsafe_allow_html=True)

                print(f"Title: {article['title']}")
                for line in report.split('\n'):
                    print(line)
                print("------------------------------------------------------------------------------------------------------------")
