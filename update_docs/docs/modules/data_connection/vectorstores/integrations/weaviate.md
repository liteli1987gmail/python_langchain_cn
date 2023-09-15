# Weaviate

>[Weaviate](https://weaviate.io/) is an open-source vector database. It allows you to store data objects and vector embeddings from your favorite ML-models, and scale seamlessly into billions of data objects.

This notebook shows how to use functionality related to the `Weaviate`vector database.

See the `Weaviate` [installation instructions](https://weaviate.io/developers/weaviate/installation).


```python
!pip install weaviate-client
```

    Requirement already satisfied: weaviate-client in /workspaces/langchain/.venv/lib/python3.9/site-packages (3.19.1)
    Requirement already satisfied: requests<2.29.0,>=2.28.0 in /workspaces/langchain/.venv/lib/python3.9/site-packages (from weaviate-client) (2.28.2)
    Requirement already satisfied: validators<=0.21.0,>=0.18.2 in /workspaces/langchain/.venv/lib/python3.9/site-packages (from weaviate-client) (0.20.0)
    Requirement already satisfied: tqdm<5.0.0,>=4.59.0 in /workspaces/langchain/.venv/lib/python3.9/site-packages (from weaviate-client) (4.65.0)
    Requirement already satisfied: authlib>=1.1.0 in /workspaces/langchain/.venv/lib/python3.9/site-packages (from weaviate-client) (1.2.0)
    Requirement already satisfied: cryptography>=3.2 in /workspaces/langchain/.venv/lib/python3.9/site-packages (from authlib>=1.1.0->weaviate-client) (40.0.2)
    Requirement already satisfied: charset-normalizer<4,>=2 in /workspaces/langchain/.venv/lib/python3.9/site-packages (from requests<2.29.0,>=2.28.0->weaviate-client) (3.1.0)
    Requirement already satisfied: idna<4,>=2.5 in /workspaces/langchain/.venv/lib/python3.9/site-packages (from requests<2.29.0,>=2.28.0->weaviate-client) (3.4)
    Requirement already satisfied: urllib3<1.27,>=1.21.1 in /workspaces/langchain/.venv/lib/python3.9/site-packages (from requests<2.29.0,>=2.28.0->weaviate-client) (1.26.15)
    Requirement already satisfied: certifi>=2017.4.17 in /workspaces/langchain/.venv/lib/python3.9/site-packages (from requests<2.29.0,>=2.28.0->weaviate-client) (2023.5.7)
    Requirement already satisfied: decorator>=3.4.0 in /workspaces/langchain/.venv/lib/python3.9/site-packages (from validators<=0.21.0,>=0.18.2->weaviate-client) (5.1.1)
    Requirement already satisfied: cffi>=1.12 in /workspaces/langchain/.venv/lib/python3.9/site-packages (from cryptography>=3.2->authlib>=1.1.0->weaviate-client) (1.15.1)
    Requirement already satisfied: pycparser in /workspaces/langchain/.venv/lib/python3.9/site-packages (from cffi>=1.12->cryptography>=3.2->authlib>=1.1.0->weaviate-client) (2.21)
    

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.


```python
import os
import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```


```python
WEAVIATE_URL = getpass.getpass("WEAVIATE_URL:")
```


```python
os.environ["WEAVIATE_API_KEY"] = getpass.getpass("WEAVIATE_API_KEY:")
```


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Weaviate
from langchain.document_loaders import TextLoader
```


```python
from langchain.document_loaders import TextLoader

loader = TextLoader("../../../state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
```


```python
db = Weaviate.from_documents(docs, embeddings, weaviate_url=WEAVIATE_URL, by_text=False)
```


```python
query = "What did the president say about Ketanji Brown Jackson"
docs = db.similarity_search(query)
```


```python
print(docs[0].page_content)
```

    Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. 
    
    Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. 
    
    One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. 
    
    And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.
    

## Similarity search with score

Sometimes we might want to perform the search, but also obtain a relevancy score to know how good is a particular result. 
The returned distance score is cosine distance. Therefore, a lower score is better.


```python
docs = db.similarity_search_with_score(query, by_text=False)
docs[0]
```




    (Document(page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'_additional': {'vector': [-0.015289668, -0.011418287, -0.018540842, 0.00274522, 0.008310737, 0.014179829, 0.0080104275, -0.0010217049, -0.022327352, -0.0055002323, 0.018958665, 0.0020548347, -0.0044393567, -0.021609223, -0.013709779, -0.004543812, 0.025722157, 0.01821442, 0.031728342, -0.031388864, -0.01051083, -0.029978717, 0.011555385, 0.0009751897, 0.014675993, -0.02102166, 0.0301354, -0.031754456, 0.013526983, -0.03392191, 0.002800712, -0.0027778621, -0.024259781, -0.006202043, -0.019950991, 0.0176138, -0.0001134321, 0.008343379, 0.034209162, -0.027654583, 0.03149332, -0.0008389079, 0.0053696632, -0.0024644958, -0.016582303, 0.0066720927, -0.005036711, -0.035514854, 0.002942706, 0.02958701, 0.032825127, 0.015694432, -0.019846536, -0.024520919, -0.021974817, -0.0063293483, -0.01081114, -0.0084282495, 0.003025944, -0.010210521, 0.008780787, 0.014793505, -0.006486031, 0.011966679, 0.01774437, -0.006985459, -0.015459408, 0.01625588, -0.016007798, 0.01706541, 0.035567082, 0.0029900377, 0.021543937, -0.0068483613, 0.040868197, -0.010909067, -0.03339963, 0.010954766, -0.014689049, -0.021596165, 0.0025607906, -0.01599474, -0.017757427, -0.0041651614, 0.010752384, 0.0053598704, -0.00019248774, 0.008480477, -0.010517359, -0.005017126, 0.0020434097, 0.011699011, 0.0051379027, 0.021687564, -0.010830725, 0.020734407, -0.006606808, 0.029769806, 0.02817686, -0.047318324, 0.024338122, -0.001150642, -0.026231378, -0.012325744, -0.0318328, -0.0094989175, -0.00897664, 0.004736402, 0.0046482678, 0.0023241339, -0.005826656, 0.0072531262, 0.015498579, -0.0077819317, -0.011953622, -0.028934162, -0.033974137, -0.01574666, 0.0086306315, -0.029299757, 0.030213742, -0.0033148287, 0.013448641, -0.013474754, 0.015851116, 0.0076578907, -0.037421167, -0.015185213, 0.010719741, -0.014636821, 0.0001918757, 0.011783881, 0.0036330915, -0.02132197, 0.0031010215, 0.0024334856, -0.0033229894, 0.050086394, 0.0031973163, -0.01115062, 0.004837593, 0.01298512, -0.018645298, -0.02992649, 0.004837593, 0.0067634913, 0.02992649, 0.0145062525, 0.00566018, -0.0017055618, -0.0056667086, 0.012697867, 0.0150677, -0.007559964, -0.01991182, -0.005268472, -0.008650217, -0.008702445, 0.027550127, 0.0018296026, 0.0018589807, -0.033295177, 0.0036265631, -0.0060290387, 0.014349569, 0.019898765, 0.00023339267, 0.0034568228, -0.018958665, 0.012031963, 0.005186866, 0.020747464, -0.03817847, 0.028202975, -0.01340947, 0.00091643346, 0.014884903, -0.02314994, -0.024468692, 0.0004859627, 0.018828096, 0.012906778, 0.027941836, 0.027550127, -0.015028529, 0.018606128, 0.03449641, -0.017757427, -0.016020855, -0.012142947, 0.025304336, 0.00821281, -0.0025461016, -0.01902395, -0.635507, -0.030083172, 0.0177052, -0.0104912445, 0.012502013, -0.0010747487, 0.00465806, 0.020825805, -0.006887532, 0.013892576, -0.019977106, 0.029952602, 0.0012004217, -0.015211326, -0.008708973, -0.017809656, 0.008578404, -0.01612531, 0.022614606, -0.022327352, -0.032616217, 0.0050693536, -0.020629952, -0.01357921, 0.011477043, 0.0013938275, -0.0052390937, 0.0142581705, -0.013200559, 0.013252786, -0.033582427, 0.030579336, -0.011568441, 0.0038387382, 0.049564116, 0.016791213, -0.01991182, 0.010889481, -0.0028251936, 0.035932675, -0.02183119, -0.008611047, 0.025121538, 0.008349908, 0.00035641342, 0.009028868, 0.007631777, -0.01298512, -0.0015350056, 0.009982024, -0.024207553, -0.003332782, 0.006283649, 0.01868447, -0.010732798, -0.00876773, -0.0075273216, -0.016530076, 0.018175248, 0.016020855, -0.00067284, 0.013461698, -0.0065904865, -0.017809656, -0.014741276, 0.016582303, -0.0088526, 0.0046482678, 0.037473395, -0.02237958, 0.010112594, 0.022549322, 9.680491e-05, -0.0059082615, 0.020747464, -0.026923396, 0.01162067, -0.0074816225, 0.00024277734, 0.011842638, 0.016921783, -0.019285088, 0.005565517, 0.0046907025, 0.018109964, 0.0028676286, -0.015080757, -0.01536801, 0.0024726565, 0.020943318, 0.02187036, 0.0037767177, 0.018997835, -0.026766712, 0.005026919, 0.015942514, 0.0097469995, -0.0067830766, 0.023828901, -0.01523744, -0.0121494755, 0.00744898, 0.010445545, -0.011006993, -0.0032789223, 0.020394927, -0.017796598, -0.0029116957, 0.02318911, -0.031754456, -0.018188305, -0.031441092, -0.030579336, 0.0011832844, 0.0065023527, -0.027053965, 0.009198609, 0.022079272, -0.027785152, 0.005846241, 0.013500868, 0.016699815, 0.010445545, -0.025265165, -0.004396922, 0.0076774764, 0.014597651, -0.009851455, -0.03637661, 0.0004745379, -0.010112594, -0.009205136, 0.01578583, 0.015211326, -0.0011653311, -0.0015847852, 0.01489796, -0.01625588, -0.0029067993, -0.011411758, 0.0046286825, 0.0036330915, -0.0034143878, 0.011894866, -0.03658552, 0.007266183, -0.015172156, -0.02038187, -0.033739112, 0.0018948873, -0.011379116, -0.0020923733, -0.014075373, 0.01970291, 0.0020352493, -0.0075273216, -0.02136114, 0.0027974476, -0.009577259, -0.023815846, 0.024847344, 0.014675993, -0.019454828, -0.013670608, 0.011059221, -0.005438212, 0.0406854, 0.0006218364, -0.024494806, -0.041259903, 0.022013986, -0.0040019494, -0.0052097156, 0.015798887, 0.016190596, 0.0003794671, -0.017444061, 0.012325744, 0.024769, 0.029482553, -0.0046547963, -0.015955571, -0.018397218, -0.0102431625, 0.020577725, 0.016190596, -0.02038187, 0.030030945, -0.01115062, 0.0032560725, -0.014819618, 0.005647123, -0.0032560725, 0.0038909658, 0.013311543, 0.024285894, -0.0045699263, -0.010112594, 0.009237779, 0.008728559, 0.0423828, 0.010909067, 0.04225223, -0.031806685, -0.013696723, -0.025787441, 0.00838255, -0.008715502, 0.006776548, 0.01825359, -0.014480138, -0.014427911, -0.017600743, -0.030004831, 0.0145845935, 0.013762007, -0.013226673, 0.004168425, 0.0047951583, -0.026923396, 0.014675993, 0.0055851024, 0.015616091, -0.012306159, 0.007670948, 0.038439605, -0.015759716, 0.00016178355, 0.01076544, -0.008232395, -0.009942854, 0.018801982, -0.0025314125, 0.030709906, -0.001442791, -0.042617824, -0.007409809, -0.013109161, 0.031101612, 0.016229765, 0.006162872, 0.017901054, -0.0063619902, -0.0054577976, 0.01872364, -0.0032430156, 0.02966535, 0.006495824, 0.0011008625, -0.00024318536, -0.007011573, -0.002746852, -0.004298995, 0.007710119, 0.03407859, -0.008898299, -0.008565348, 0.030527107, -0.0003027576, 0.025082368, 0.0405026, 0.03867463, 0.0014117807, -0.024076983, 0.003933401, -0.009812284, 0.00829768, -0.0074293944, 0.0061530797, -0.016647588, -0.008147526, -0.015629148, 0.02055161, 0.000504324, 0.03157166, 0.010112594, -0.009009283, 0.026557801, -0.013997031, -0.0071878415, 0.009414048, -0.03480978, 0.006626393, 0.013827291, -0.011444401, -0.011823053, -0.0042957305, -0.016229765, -0.014192886, 0.026531687, -0.012534656, -0.0056569157, -0.0010331298, 0.007977786, 0.0033654245, -0.017352663, 0.034626983, -0.011803466, 0.009035396, 0.0005288057, 0.020421041, 0.013115689, -0.0152504975, -0.0111114485, 0.032355078, 0.0025542623, -0.0030226798, -0.00074261305, 0.030892702, -0.026218321, 0.0062803845, -0.018031623, -0.021504767, -0.012834964, 0.009009283, -0.0029198565, -0.014349569, -0.020434098, 0.009838398, -0.005993132, -0.013618381, -0.031597774, -0.019206747, 0.00086583785, 0.15835446, 0.033765227, 0.00893747, 0.015119928, -0.019128405, 0.0079582, -0.026270548, -0.015877228, 0.014153715, -0.011960151, 0.007853745, 0.006972402, -0.014101488, 0.02456009, 0.015119928, -0.0018850947, 0.019010892, -0.0046188897, -0.0050954674, -0.03548874, -0.01608614, -0.00324628, 0.009466276, 0.031911142, 7.033402e-05, -0.025095424, 0.020225188, 0.014832675, 0.023228282, -0.011829581, -0.011300774, -0.004073763, 0.0032544404, -0.0025983294, -0.020943318, 0.019650683, -0.0074424515, -0.0030977572, 0.0073379963, -0.00012455089, 0.010230106, -0.0007254758, -0.0025052987, -0.009681715, 0.03439196, -0.035123147, -0.0028806855, 0.012828437, 0.00018646932, 0.0066133365, 0.025539361, -0.00055736775, -0.025356563, -0.004537284, -0.007031158, 0.015825002, -0.013076518, 0.00736411, -0.00075689406, 0.0076578907, -0.019337315, -0.0024187965, -0.0110331075, -0.01187528, 0.0013048771, 0.0009711094, -0.027863493, -0.020616895, -0.0024481746, -0.0040802914, 0.014571536, -0.012306159, -0.037630077, 0.012652168, 0.009068039, -0.0018263385, 0.0371078, -0.0026831995, 0.011333417, -0.011548856, -0.0059049972, -0.025186824, 0.0069789304, -0.010993936, -0.0009066408, 0.0002619547, 0.01727432, -0.008082241, -0.018645298, 0.024507863, 0.0030895968, -0.0014656406, 0.011137563, -0.025513247, -0.022967143, -0.002033617, 0.006887532, 0.016621474, -0.019337315, -0.0030618508, 0.0014697209, -0.011679426, -0.003597185, -0.0049844836, -0.012332273, 0.009068039, 0.009407519, 0.027080078, -0.011215905, -0.0062542707, -0.0013114056, -0.031911142, 0.011209376, 0.009903682, -0.007351053, 0.021335026, -0.005510025, 0.0062053073, -0.010869896, -0.0045601334, 0.017561574, -0.024847344, 0.04115545, -0.00036457402, -0.0061400225, 0.013037347, -0.005480647, 0.005947433, 0.020799693, 0.014702106, 0.03272067, 0.026701428, -0.015550806, -0.036193814, -0.021126116, -0.005412098, -0.013076518, 0.027080078, 0.012900249, -0.0073379963, -0.015119928, -0.019781252, 0.0062346854, -0.03266844, 0.025278222, -0.022797402, -0.0028415148, 0.021452539, -0.023162996, 0.005170545, -0.022314297, 0.011215905, -0.009838398, -0.00033233972, 0.0019650683, 0.0026326037, 0.009753528, -0.0029639236, 0.021126116, 0.01944177, -0.00044883206, -0.00961643, 0.008846072, -0.0035775995, 0.02352859, -0.0020956376, 0.0053468137, 0.013305014, 0.0006418298, 0.023802789, 0.013122218, -0.0031548813, -0.027471786, 0.005046504, 0.008545762, 0.011261604, -0.01357921, -0.01110492, -0.014845733, -0.035384286, -0.02550019, 0.008154054, -0.0058331843, -0.008702445, -0.007311882, -0.006525202, 0.03817847, 0.00372449, 0.022914914, -0.0018981516, 0.031545546, -0.01051083, 0.013801178, -0.006296706, -0.00025052988, -0.01795328, -0.026296662, 0.0017659501, 0.021883417, 0.0028937424, 0.00495837, -0.011888337, -0.008950527, -0.012058077, 0.020316586, 0.00804307, -0.0068483613, -0.0038387382, 0.019715967, -0.025069311, -0.000797697, -0.04507253, -0.009179023, -0.016242823, 0.013553096, -0.0019014158, 0.010223578, 0.0062934416, -5.5644974e-05, -0.038282923, -0.038544063, -0.03162389, -0.006815719, 0.009936325, 0.014192886, 0.02277129, -0.006972402, -0.029769806, 0.034862008, 0.01217559, -0.0037179615, 0.0008666539, 0.008924413, -0.026296662, -0.012678281, 0.014480138, 0.020734407, -0.012103776, -0.037499506, 0.022131499, 0.015028529, -0.033843566, 0.00020187242, 0.002650557, -0.0015113399, 0.021570051, -0.008284623, -0.003793039, -0.013422526, -0.009655601, -0.0016614947, -0.02388113, 0.00114901, 0.0034405016, 0.02796795, -0.039118566, 0.0023975791, -0.010608757, 0.00093438674, 0.0017382042, -0.02047327, 0.026283605, -0.020799693, 0.005947433, -0.014349569, 0.009890626, -0.022719061, -0.017248206, 0.0042565595, 0.022327352, -0.015681375, -0.013840348, 6.502964e-05, 0.015485522, -0.002678303, -0.0047984226, -0.012182118, -0.001512972, 0.013931747, -0.009642544, 0.012652168, -0.012932892, -0.027759038, -0.01085031, 0.0050236546, -0.009675186, -0.00893747, -0.0051770736, 0.036011018, 0.003528636, -0.001008648, -0.015811944, -0.008865656, 0.012364916, 0.016621474, -0.01340947, 0.03219839, 0.032955695, -0.021517823, 0.00372449, -0.045124754, 0.015589978, -0.033582427, -0.01642562, -0.009609901, -0.031179955, 0.0012591778, -0.011176733, -0.018658355, -0.015224383, 0.014884903, 0.013083046, 0.0063587264, -0.008238924, -0.008917884, -0.003877909, 0.022836573, -0.004374072, -0.031127727, 0.02604858, -0.018136078, 0.000769951, -0.002312709, -0.025095424, -0.010621814, 0.013207087, 0.013944804, -0.0070899143, -0.022183727, -0.0028088724, -0.011424815, 0.026087752, -0.0058625625, -0.020186016, -0.010217049, 0.015315781, -0.012580355, 0.01374895, 0.004948577, -0.0021854038, 0.023215225, 0.00207442, 0.029639237, 0.01391869, -0.015811944, -0.005356606, -0.022327352, -0.021844247, -0.008310737, -0.020786636, -0.022484036, 0.011411758, 0.005826656, 0.012188647, -0.020394927, -0.0013024289, -0.027315103, -0.017000126, -0.0010600596, -0.0019014158, 0.016712872, 0.0012673384, 0.02966535, 0.02911696, -0.03081436, 0.025552418, 0.0014215735, -0.02510848, 0.020277414, -0.02672754, 0.01829276, 0.03381745, -0.013957861, 0.0049094064, 0.033556316, 0.005167281, 0.0176138, 0.014140658, -0.0043708077, -0.0095446175, 0.012952477, 0.007853745, -0.01034109, 0.01804468, 0.0038322096, -0.04959023, 0.0023078127, 0.0053794556, -0.015106871, -0.03225062, -0.010073422, 0.007285768, 0.0056079524, -0.009002754, -0.014362626, 0.010909067, 0.009779641, -0.02796795, 0.013246258, 0.025474075, -0.001247753, 0.02442952, 0.012802322, -0.032276735, 0.0029802448, 0.014179829, 0.010321504, 0.0053337566, -0.017156808, -0.010439017, 0.034444187, -0.010393318, -0.006042096, -0.018566957, 0.004517698, -0.011228961, -0.009015812, -0.02089109, 0.022484036, 0.0029867734, -0.029064732, -0.010236635, -0.0006761042, -0.029038617, 0.004367544, -0.012293102, 0.0017528932, -0.023358852, 0.02217067, 0.012606468, -0.008160583, -0.0104912445, -0.0034894652, 0.011078807, 0.00050922035, 0.015759716, 0.23774062, -0.0019291617, 0.006218364, 0.013762007, -0.029900376, 0.018188305, 0.0092965355, 0.0040574414, -0.014976301, -0.006228157, -0.016647588, 0.0035188433, -0.01919369, 0.0037506039, 0.029247528, -0.014532366, -0.049773026, -0.019624569, -0.034783665, -0.015028529, 0.0097469995, 0.016281994, 0.0047135525, -0.011294246, 0.011477043, 0.015485522, 0.03426139, 0.014323455, 0.011052692, -0.008362965, -0.037969556, -0.00252162, -0.013709779, -0.0030292084, -0.016569246, -0.013879519, 0.0011849166, -0.0016925049, 0.009753528, 0.008349908, -0.008245452, 0.033007924, -0.0035873922, -0.025461018, 0.016791213, 0.05410793, -0.005950697, -0.011672897, -0.0072335405, 0.013814235, -0.0593307, -0.008624103, 0.021400312, 0.034235276, 0.015642203, -0.020068504, 0.03136275, 0.012567298, -0.010419431, 0.027445672, -0.031754456, 0.014219, -0.0075403787, 0.03812624, 0.0009988552, 0.038752973, -0.018005509, 0.013670608, 0.045882057, -0.018841153, -0.031650003, 0.010628343, -0.00459604, -0.011999321, -0.028202975, -0.018593071, 0.029743692, 0.021857304, 0.01438874, 0.00014128008, -0.006156344, -0.006691678, 0.01672593, -0.012821908, -0.0024367499, -0.03219839, 0.0058233915, -0.0056405943, -0.009381405, 0.0064044255, 0.013905633, -0.011228961, -0.0013481282, -0.014023146, 0.00016239559, -0.0051901303, 0.0025265163, 0.023619989, -0.021517823, 0.024703717, -0.025643816, 0.040189236, 0.016295051, -0.0040411204, -0.0113595305, 0.0029981981, -0.015589978, 0.026479458, 0.0067439056, -0.035775993, -0.010550001, -0.014767391, -0.009897154, -0.013944804, -0.0147543335, 0.015798887, -0.02456009, -0.0018850947, 0.024442578, 0.0019715966, -0.02422061, -0.02945644, -0.003443766, 0.0004945313, 0.0011522742, -0.020773578, -0.011777353, 0.008173639, -0.012325744, -0.021348083, 0.0036461484, 0.0063228197, 0.00028970066, -0.0036200345, -0.021596165, -0.003949722, -0.0006034751, 0.007305354, -0.023424136, 0.004834329, -0.008833014, -0.013435584, 0.0026097542, -0.0012240873, -0.0028349862, -0.01706541, 0.027863493, -0.026414175, -0.011783881, 0.014075373, -0.005634066, -0.006313027, -0.004638475, -0.012495484, 0.022836573, -0.022719061, -0.031284407, -0.022405695, -0.017352663, 0.021113059, -0.03494035, 0.002772966, 0.025643816, -0.0064240107, -0.009897154, 0.0020711557, -0.16409951, 0.009688243, 0.010393318, 0.0033262535, 0.011059221, -0.012919835, 0.0014493194, -0.021857304, -0.0075730206, -0.0020695236, 0.017822713, 0.017417947, -0.034835894, -0.009159437, -0.0018573486, -0.0024840813, -0.022444865, 0.0055687814, 0.0037767177, 0.0033915383, 0.0301354, -0.012227817, 0.0021854038, -0.042878963, 0.021517823, -0.010419431, -0.0051183174, 0.01659536, 0.0017333078, -0.00727924, -0.0020026069, -0.0012493852, 0.031441092, 0.0017431005, 0.008702445, -0.0072335405, -0.020081561, -0.012423672, -0.0042239176, 0.031049386, 0.04324456, 0.02550019, 0.014362626, -0.0107393265, -0.0037538682, -0.0061791935, -0.006737377, 0.011548856, -0.0166737, -0.012828437, -0.003375217, -0.01642562, -0.011424815, 0.007181313, 0.017600743, -0.0030226798, -0.014192886, 0.0128937205, -0.009975496, 0.0051444313, -0.0044654706, -0.008826486, 0.004158633, 0.004971427, -0.017835768, 0.025017083, -0.021792019, 0.013657551, -0.01872364, 0.009100681, -0.0079582, -0.011640254, -0.01093518, -0.0147543335, -0.005000805, 0.02345025, -0.028908048, 0.0104912445, -0.00753385, 0.017561574, -0.012025435, 0.042670052, -0.0041978033, 0.0013056932, -0.009263893, -0.010941708, -0.004471999, 0.01008648, -0.002578744, -0.013931747, 0.018619185, -0.04029369, -0.00025909848, 0.0030063589, 0.003149985, 0.011091864, 0.006495824, 0.00026583098, 0.0045503406, -0.007586078, -0.0007475094, -0.016856499, -0.003528636, 0.038282923, -0.0010494508, 0.024494806, 0.012593412, 0.032433417, -0.003203845, 0.005947433, -0.019937934, -0.00017800271, 0.027706811, 0.03047488, 0.02047327, 0.0019258976, -0.0068940604, -0.0014990991, 0.013305014, -0.007690533, 0.058808424, -0.0016859764, -0.0044622063, -0.0037734534, 0.01578583, -0.0018459238, -0.1196015, -0.0007075225, 0.0030341048, 0.012306159, -0.0068483613, 0.01851473, 0.015315781, 0.031388864, -0.015563863, 0.04776226, -0.008199753, -0.02591801, 0.00546759, -0.004915935, 0.0050824108, 0.0027011528, -0.009205136, -0.016712872, -0.0033409426, 0.0043218443, -0.018279705, 0.00876773, 0.0050138617, -0.009688243, -0.017783541, -0.018645298, -0.010380261, 0.018606128, 0.0077492893, 0.007324939, -0.012704396, -0.002692992, -0.01259994, -0.0076970616, -0.013814235, -0.0004365912, -0.023606932, -0.020186016, 0.025330449, -0.00991674, -0.0048278007, -0.019350372, 0.015433294, -0.0056144805, -0.0034927295, -0.00043455104, 0.008611047, 0.025748271, 0.022353467, -0.020747464, -0.015759716, 0.029038617, -0.000377631, -0.028725252, 0.018109964, -0.0016125311, -0.022719061, -0.009133324, -0.033060152, 0.011248547, -0.0019797573, -0.007181313, 0.0018867267, 0.0070899143, 0.004077027, 0.0055328747, -0.014245113, -0.021217514, -0.006750434, -0.038230695, 0.013233202, 0.014219, -0.017692143, 0.024742888, -0.008833014, -0.00753385, -0.026923396, -0.0021527617, 0.013135274, -0.018070793, -0.013500868, -0.0016696552, 0.011568441, -0.03230285, 0.023646105, 0.0111114485, -0.015172156, 0.0257091, 0.0045699263, -0.00919208, 0.021517823, 0.037838988, 0.00787333, -0.007755818, -0.028281316, 0.011170205, -0.005412098, -0.016321165, 0.009929797, 0.004609097, -0.03047488, 0.002688096, -0.07264877, 0.024455635, -0.020930262, -0.015381066, -0.0033148287, 0.027236762, 0.0014501355, -0.014101488, -0.024076983, 0.026218321, -0.009009283, 0.019624569, 0.0020646274, -0.009081096, -0.01565526, -0.003358896, 0.048571788, -0.004857179, 0.022444865, 0.024181439, 0.00080708164, 0.024873456, 3.463147e-05, 0.0010535312, -0.017940223, 0.0012159267, -0.011065749, 0.008258509, -0.018527785, -0.022797402, 0.012377972, -0.002087477, 0.010791554, 0.022288183, 0.0048604426, -0.032590102, 0.013709779, 0.004922463, 0.020055447, -0.0150677, -0.0057222005, -0.036246043, 0.0021364405, 0.021387255, -0.013435584, 0.010732798, 0.0075534354, -0.00061612396, -0.002018928, -0.004432828, -0.032746784, 0.025513247, -0.0025852725, 0.014467081, -0.008617575, -0.019755138, 0.003966043, -0.0033915383, 0.0004088452, -0.025173767, 0.02796795, 0.0023763615, 0.0052358294, 0.017796598, 0.014806561, 0.0150024155, -0.005859298, 0.01259994, 0.021726735, -0.026466403, -0.017457118, -0.0025493659, 0.0070899143, 0.02668837, 0.015485522, -0.011588027, 0.01906312, -0.003388274, -0.010210521, 0.020956375, 0.028620796, -0.018540842, 0.0025722156, 0.0110331075, -0.003992157, 0.020930262, 0.008487006, 0.0016557822, -0.0009882465, 0.0062640635, -0.016242823, -0.0007785196, -0.0007213955, 0.018971723, 0.021687564, 0.0039464575, -0.01574666, 0.011783881, -0.0019797573, -0.013383356, -0.002706049, 0.0037734534, 0.020394927, -0.00021931567, 0.0041814824, 0.025121538, -0.036246043, -0.019428715, -0.023802789, 0.014845733, 0.015420238, 0.019650683, 0.008186696, 0.025304336, -0.03204171, 0.01774437, 0.0021233836, -0.008434778, -0.0059441687, 0.038335152, 0.022653777, -0.0066002794, 0.02149171, 0.015093814, 0.025382677, -0.007579549, 0.0030357367, -0.0014117807, -0.015341896, 0.014545423, 0.007135614, -0.0113595305, -0.04387129, 0.016308108, -0.008186696, -0.013370299, -0.014297341, 0.017431004, -0.022666834, 0.039458048, 0.0032005806, -0.02081275, 0.008526176, -0.0019307939, 0.024024757, 0.009068039, 0.00953156, 0.010608757, 0.013801178, 0.035932675, -0.015185213, -0.0038322096, -0.012462842, -0.03655941, 0.0013946436, 0.00025726235, 0.008016956, -0.0042565595, 0.008447835, 0.0038191527, -0.014702106, 0.02196176, 0.0052097156, -0.010869896, 0.0051640165, 0.030840475, -0.041468814, 0.009250836, -0.018997835, 0.020107675, 0.008421721, -0.016373392, 0.004602568, 0.0327729, -0.00812794, 0.001581521, 0.019350372, 0.016112253, 0.02132197, 0.00043944738, -0.01472822, -0.025735214, -0.03313849, 0.0033817457, 0.028855821, -0.016033912, 0.0050791465, -0.01808385]}, 'source': '../../../state_of_the_union.txt'}),
     0.8154189703772676)



# Persistance

Anything uploaded to weaviate is automatically persistent into the database. You do not need to call any specific method or pass any param for this to happen.

# Retriever options

## Retriever options

This section goes over different options for how to use Weaviate as a retriever.

### MMR

In addition to using similarity search in the retriever object, you can also use `mmr`.


```python
retriever = db.as_retriever(search_type="mmr")
retriever.get_relevant_documents(query)[0]
```




    Document(page_content='Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you’re at it, pass the Disclose Act so Americans can know who is funding our elections. \n\nTonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service. \n\nOne of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court. \n\nAnd I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation’s top legal minds, who will continue Justice Breyer’s legacy of excellence.', metadata={'source': '../../../state_of_the_union.txt'})



## Question Answering with Sources

This section goes over how to do question-answering with sources over an Index. It does this by using the `RetrievalQAWithSourcesChain`, which does the lookup of the documents from an Index. 


```python
from langchain.chains import RetrievalQAWithSourcesChain
from langchain import OpenAI
```


```python
with open("../../../state_of_the_union.txt") as f:
    state_of_the_union = f.read()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(state_of_the_union)
```


```python
docsearch = Weaviate.from_texts(
    texts,
    embeddings,
    weaviate_url=WEAVIATE_URL,
    by_text=False,
    metadatas=[{"source": f"{i}-pl"} for i in range(len(texts))],
)
```


```python
chain = RetrievalQAWithSourcesChain.from_chain_type(
    OpenAI(temperature=0), chain_type="stuff", retriever=docsearch.as_retriever()
)
```


```python
chain(
    {"question": "What did the president say about Justice Breyer"},
    return_only_outputs=True,
)
```




    {'answer': " The president honored Justice Breyer for his service and mentioned his legacy of excellence. He also nominated Circuit Court of Appeals Judge Ketanji Brown Jackson to continue Justice Breyer's legacy.\n",
     'sources': '31-pl, 34-pl'}

