# Analysis of Twitter the-algorithm source code with LangChain, GPT4 and Deep Lake
In this tutorial, we are going to use Langchain + Deep Lake with GPT4 to analyze the code base of the twitter algorithm. 


```python
!python3 -m pip install --upgrade langchain deeplake openai tiktoken
```

Define OpenAI embeddings, Deep Lake multi-modal vector store api and authenticate. For full documentation of Deep Lake please follow [docs](https://docs.activeloop.ai/) and [API reference](https://docs.deeplake.ai/en/latest/).

Authenticate into Deep Lake if you want to create your own dataset and publish it. You can get an API key from the [platform](https://app.activeloop.ai)


```python
import os
import getpass

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
os.environ["ACTIVELOOP_TOKEN"] = getpass.getpass("Activeloop Token:")
```


```python
embeddings = OpenAIEmbeddings(disallowed_special=())
```

disallowed_special=() is required to avoid `Exception: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte` from tiktoken for some repositories

### 1. Index the code base (optional)
You can directly skip this part and directly jump into using already indexed dataset. To begin with, first we will clone the repository, then parse and chunk the code base and use OpenAI indexing.


```python
!git clone https://github.com/twitter/the-algorithm # replace any repository of your choice
```

Load all files inside the repository


```python
import os
from langchain.document_loaders import TextLoader

root_dir = "./the-algorithm"
docs = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    for file in filenames:
        try:
            loader = TextLoader(os.path.join(dirpath, file), encoding="utf-8")
            docs.extend(loader.load_and_split())
        except Exception as e:
            pass
```

Then, chunk the files


```python
from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)
```

Execute the indexing. This will take about ~4 mins to compute embeddings and upload to Activeloop. You can then publish the dataset to be public.


```python
username = "davitbun"  # replace with your username from app.activeloop.ai
db = DeepLake(
    dataset_path=f"hub://{username}/twitter-algorithm",
    embedding_function=embeddings,
)
db.add_documents(texts)
```

### 2. Question Answering on Twitter algorithm codebase
First load the dataset, construct the retriever, then construct the Conversational Chain


```python
db = DeepLake(
    dataset_path="hub://davitbun/twitter-algorithm",
    read_only=True,
    embedding_function=embeddings,
)
```

    Deep Lake Dataset in hub://davitbun/twitter-algorithm already exists, loading from the storage
    


```python
retriever = db.as_retriever()
retriever.search_kwargs["distance_metric"] = "cos"
retriever.search_kwargs["fetch_k"] = 100
retriever.search_kwargs["maximal_marginal_relevance"] = True
retriever.search_kwargs["k"] = 10
```

You can also specify user defined functions using [Deep Lake filters](https://docs.deeplake.ai/en/latest/deeplake.core.dataset.html#deeplake.core.dataset.Dataset.filter)


```python
def filter(x):
    # filter based on source code
    if "com.google" in x["text"].data()["value"]:
        return False

    # filter based on path e.g. extension
    metadata = x["metadata"].data()["value"]
    return "scala" in metadata["source"] or "py" in metadata["source"]


### turn on below for custom filtering
# retriever.search_kwargs['filter'] = filter
```


```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

model = ChatOpenAI(model_name="gpt-3.5-turbo")  # switch to 'gpt-4'
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)
```


```python
questions = [
    "What does favCountParams do?",
    "is it Likes + Bookmarks, or not clear from the code?",
    "What are the major negative modifiers that lower your linear ranking parameters?",
    "How do you get assigned to SimClusters?",
    "What is needed to migrate from one SimClusters to another SimClusters?",
    "How much do I get boosted within my cluster?",
    "How does Heavy ranker work. what are it’s main inputs?",
    "How can one influence Heavy ranker?",
    "why threads and long tweets do so well on the platform?",
    "Are thread and long tweet creators building a following that reacts to only threads?",
    "Do you need to follow different strategies to get most followers vs to get most likes and bookmarks per tweet?",
    "Content meta data and how it impacts virality (e.g. ALT in images).",
    "What are some unexpected fingerprints for spam factors?",
    "Is there any difference between company verified checkmarks and blue verified individual checkmarks?",
]
chat_history = []

for question in questions:
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    print(f"-> **Question**: {question} \n")
    print(f"**Answer**: {result['answer']} \n")
```

-> **Question**: What does favCountParams do? 

**Answer**: `favCountParams` is an optional ThriftLinearFeatureRankingParams instance that represents the parameters related to the "favorite count" feature in the ranking process. It is used to control the weight of the favorite count feature while ranking tweets. The favorite count is the number of times a tweet has been marked as a favorite by users, and it is considered an important signal in the ranking of tweets. By using `favCountParams`, the system can adjust the importance of the favorite count while calculating the final ranking score of a tweet. 

-> **Question**: is it Likes + Bookmarks, or not clear from the code?

**Answer**: From the provided code, it is not clear if the favorite count metric is determined by the sum of likes and bookmarks. The favorite count is mentioned in the code, but there is no explicit reference to how it is calculated in terms of likes and bookmarks. 

-> **Question**: What are the major negative modifiers that lower your linear ranking parameters?

**Answer**: In the given code, major negative modifiers that lower the linear ranking parameters are:

1. `scoringData.querySpecificScore`: This score adjustment is based on the query-specific information. If its value is negative, it will lower the linear ranking parameters.

2. `scoringData.authorSpecificScore`: This score adjustment is based on the author-specific information. If its value is negative, it will also lower the linear ranking parameters.

Please note that I cannot provide more information on the exact calculations of these negative modifiers, as the code for their determination is not provided. 

-> **Question**: How do you get assigned to SimClusters?

**Answer**: The assignment to SimClusters occurs through a Metropolis-Hastings sampling-based community detection algorithm that is run on the Producer-Producer similarity graph. This graph is created by computing the cosine similarity scores between the users who follow each producer. The algorithm identifies communities or clusters of Producers with similar followers, and takes a parameter *k* for specifying the number of communities to be detected.

After the community detection, different users and content are represented as sparse, interpretable vectors within these identified communities (SimClusters). The resulting SimClusters embeddings can be used for various recommendation tasks. 

-> **Question**: What is needed to migrate from one SimClusters to another SimClusters?

**Answer**: To migrate from one SimClusters representation to another, you can follow these general steps:

1. **Prepare the new representation**: Create the new SimClusters representation using any necessary updates or changes in the clustering algorithm, similarity measures, or other model parameters. Ensure that this new representation is properly stored and indexed as needed.

2. **Update the relevant code and configurations**: Modify the relevant code and configuration files to reference the new SimClusters representation. This may involve updating paths or dataset names to point to the new representation, as well as changing code to use the new clustering method or similarity functions if applicable.

3. **Test the new representation**: Before deploying the changes to production, thoroughly test the new SimClusters representation to ensure its effectiveness and stability. This may involve running offline jobs like candidate generation and label candidates, validating the output, as well as testing the new representation in the evaluation environment using evaluation tools like TweetSimilarityEvaluationAdhocApp.

4. **Deploy the changes**: Once the new representation has been tested and validated, deploy the changes to production. This may involve creating a zip file, uploading it to the packer, and then scheduling it with Aurora. Be sure to monitor the system to ensure a smooth transition between representations and verify that the new representation is being used in recommendations as expected.

5. **Monitor and assess the new representation**: After the new representation has been deployed, continue to monitor its performance and impact on recommendations. Take note of any improvements or issues that arise and be prepared to iterate on the new representation if needed. Always ensure that the results and performance metrics align with the system's goals and objectives. 

-> **Question**: How much do I get boosted within my cluster?

**Answer**: It's not possible to determine the exact amount your content is boosted within your cluster in the SimClusters representation without specific data about your content and its engagement metrics. However, a combination of factors, such as the favorite score and follow score, alongside other engagement signals and SimCluster calculations, influence the boosting of content. 

-> **Question**: How does Heavy ranker work. what are it’s main inputs?

**Answer**: The Heavy Ranker is a machine learning model that plays a crucial role in ranking and scoring candidates within the recommendation algorithm. Its primary purpose is to predict the likelihood of a user engaging with a tweet or connecting with another user on the platform.

Main inputs to the Heavy Ranker consist of:

1. Static Features: These are features that can be computed directly from a tweet at the time it's created, such as whether it has a URL, has cards, has quotes, etc. These features are produced by the Index Ingester as the tweets are generated and stored in the index.

2. Real-time Features: These per-tweet features can change after the tweet has been indexed. They mostly consist of social engagements like retweet count, favorite count, reply count, and some spam signals that are computed with later activities. The Signal Ingester, which is part of a Heron topology, processes multiple event streams to collect and compute these real-time features.

3. User Table Features: These per-user features are obtained from the User Table Updater that processes a stream written by the user service. This input is used to store sparse real-time user information, which is later propagated to the tweet being scored by looking up the author of the tweet.

4. Search Context Features: These features represent the context of the current searcher, like their UI language, their content consumption, and the current time (implied). They are combined with Tweet Data to compute some of the features used in scoring.

These inputs are then processed by the Heavy Ranker to score and rank candidates based on their relevance and likelihood of engagement by the user. 

-> **Question**: How can one influence Heavy ranker?

**Answer**: To influence the Heavy Ranker's output or ranking of content, consider the following actions:

1. Improve content quality: Create high-quality and engaging content that is relevant, informative, and valuable to users. High-quality content is more likely to receive positive user engagement, which the Heavy Ranker considers when ranking content.

2. Increase user engagement: Encourage users to interact with content through likes, retweets, replies, and comments. Higher engagement levels can lead to better ranking in the Heavy Ranker's output.

3. Optimize your user profile: A user's reputation, based on factors such as their follower count and follower-to-following ratio, may impact the ranking of their content. Maintain a good reputation by following relevant users, keeping a reasonable follower-to-following ratio and engaging with your followers.

4. Enhance content discoverability: Use relevant keywords, hashtags, and mentions in your tweets, making it easier for users to find and engage with your content. This increased discoverability may help improve the ranking of your content by the Heavy Ranker.

5. Leverage multimedia content: Experiment with different content formats, such as videos, images, and GIFs, which may capture users' attention and increase engagement, resulting in better ranking by the Heavy Ranker.

6. User feedback: Monitor and respond to feedback for your content. Positive feedback may improve your ranking, while negative feedback provides an opportunity to learn and improve.

Note that the Heavy Ranker uses a combination of machine learning models and various features to rank the content. While the above actions may help influence the ranking, there are no guarantees as the ranking process is determined by a complex algorithm, which evolves over time. 

-> **Question**: why threads and long tweets do so well on the platform?

**Answer**: Threads and long tweets perform well on the platform for several reasons:

1. **More content and context**: Threads and long tweets provide more information and context about a topic, which can make the content more engaging and informative for users. People tend to appreciate a well-structured and detailed explanation of a subject or a story, and threads and long tweets can do that effectively.

2. **Increased user engagement**: As threads and long tweets provide more content, they also encourage users to engage with the tweets through replies, retweets, and likes. This increased engagement can lead to better visibility of the content, as the Twitter algorithm considers user engagement when ranking and surfacing tweets.

3. **Narrative structure**: Threads enable users to tell stories or present arguments in a step-by-step manner, making the information more accessible and easier to follow. This narrative structure can capture users' attention and encourage them to read through the entire thread and interact with the content.

4. **Expanded reach**: When users engage with a thread, their interactions can bring the content to the attention of their followers, helping to expand the reach of the thread. This increased visibility can lead to more interactions and higher performance for the threaded tweets.

5. **Higher content quality**: Generally, threads and long tweets require more thought and effort to create, which may lead to higher quality content. Users are more likely to appreciate and interact with high-quality, well-reasoned content, further improving the performance of these tweets within the platform.

Overall, threads and long tweets perform well on Twitter because they encourage user engagement and provide a richer, more informative experience that users find valuable. 

-> **Question**: Are thread and long tweet creators building a following that reacts to only threads?

**Answer**: Based on the provided code and context, there isn't enough information to conclude if the creators of threads and long tweets primarily build a following that engages with only thread-based content. The code provided is focused on Twitter's recommendation and ranking algorithms, as well as infrastructure components like Kafka, partitions, and the Follow Recommendations Service (FRS). To answer your question, data analysis of user engagement and results of specific edge cases would be required. 

-> **Question**: Do you need to follow different strategies to get most followers vs to get most likes and bookmarks per tweet?

**Answer**: Yes, different strategies need to be followed to maximize the number of followers compared to maximizing likes and bookmarks per tweet. While there may be some overlap in the approaches, they target different aspects of user engagement.

Maximizing followers: The primary focus is on growing your audience on the platform. Strategies include:

1. Consistently sharing high-quality content related to your niche or industry.
2. Engaging with others on the platform by replying, retweeting, and mentioning other users.
3. Using relevant hashtags and participating in trending conversations.
4. Collaborating with influencers and other users with a large following.
5. Posting at optimal times when your target audience is most active.
6. Optimizing your profile by using a clear profile picture, catchy bio, and relevant links.

Maximizing likes and bookmarks per tweet: The focus is on creating content that resonates with your existing audience and encourages engagement. Strategies include:

1. Crafting engaging and well-written tweets that encourage users to like or save them.
2. Incorporating visually appealing elements, such as images, GIFs, or videos, that capture attention.
3. Asking questions, sharing opinions, or sparking conversations that encourage users to engage with your tweets.
4. Using analytics to understand the type of content that resonates with your audience and tailoring your tweets accordingly.
5. Posting a mix of educational, entertaining, and promotional content to maintain variety and interest.
6. Timing your tweets strategically to maximize engagement, likes, and bookmarks per tweet.

Both strategies can overlap, and you may need to adapt your approach by understanding your target audience's preferences and analyzing your account's performance. However, it's essential to recognize that maximizing followers and maximizing likes and bookmarks per tweet have different focuses and require specific strategies. 

-> **Question**: Content meta data and how it impacts virality (e.g. ALT in images).

**Answer**: There is no direct information in the provided context about how content metadata, such as ALT text in images, impacts the virality of a tweet or post. However, it's worth noting that including ALT text can improve the accessibility of your content for users who rely on screen readers, which may lead to increased engagement for a broader audience. Additionally, metadata can be used in search engine optimization, which might improve the visibility of the content, but the context provided does not mention any specific correlation with virality. 

-> **Question**: What are some unexpected fingerprints for spam factors?

**Answer**: In the provided context, an unusual indicator of spam factors is when a tweet contains a non-media, non-news link. If the tweet has a link but does not have an image URL, video URL, or news URL, it is considered a potential spam vector, and a threshold for user reputation (tweepCredThreshold) is set to MIN_TWEEPCRED_WITH_LINK.

While this rule may not cover all possible unusual spam indicators, it is derived from the specific codebase and logic shared in the context. 

-> **Question**: Is there any difference between company verified checkmarks and blue verified individual checkmarks?

**Answer**: Yes, there is a distinction between the verified checkmarks for companies and blue verified checkmarks for individuals. The code snippet provided mentions "Blue-verified account boost" which indicates that there is a separate category for blue verified accounts. Typically, blue verified checkmarks are used to indicate notable individuals, while verified checkmarks are for companies or organizations. 



