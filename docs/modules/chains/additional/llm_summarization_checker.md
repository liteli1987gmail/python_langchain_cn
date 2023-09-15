# Summarization checker chain
This notebook shows some examples of LLMSummarizationCheckerChain in use with different types of texts.  It has a few distinct differences from the `LLMCheckerChain`, in that it doesn't have any assumptions to the format of the input text (or summary).
Additionally, as the LLMs like to hallucinate when fact checking or get confused by context, it is sometimes beneficial to run the checker multiple times.  It does this by feeding the rewritten "True" result back on itself, and checking the "facts" for truth.  As you can see from the examples below, this can be very effective in arriving at a generally true body of text.

You can control the number of times the checker runs by setting the `max_checks` parameter.  The default is 2, but you can set it to 1 if you don't want any double-checking.


```python
from langchain.chains import LLMSummarizationCheckerChain
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)
checker_chain = LLMSummarizationCheckerChain.from_llm(llm, verbose=True, max_checks=2)
text = """
Your 9-year old might like these recent discoveries made by The James Webb Space Telescope (JWST):
• In 2023, The JWST spotted a number of galaxies nicknamed "green peas." They were given this name because they are small, round, and green, like peas.
• The telescope captured images of galaxies that are over 13 billion years old. This means that the light from these galaxies has been traveling for over 13 billion years to reach us.
• JWST took the very first pictures of a planet outside of our own solar system. These distant worlds are called "exoplanets." Exo means "from outside."
These discoveries can spark a child's imagination about the infinite wonders of the universe."""
checker_chain.run(text)
```

    
    
    [1m> Entering new LLMSummarizationCheckerChain chain...[0m
    
    
    [1m> Entering new SequentialChain chain...[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mGiven some text, extract a list of facts from the text.
    
    Format your output as a bulleted list.
    
    Text:
    """
    
    Your 9-year old might like these recent discoveries made by The James Webb Space Telescope (JWST):
    • In 2023, The JWST spotted a number of galaxies nicknamed "green peas." They were given this name because they are small, round, and green, like peas.
    • The telescope captured images of galaxies that are over 13 billion years old. This means that the light from these galaxies has been traveling for over 13 billion years to reach us.
    • JWST took the very first pictures of a planet outside of our own solar system. These distant worlds are called "exoplanets." Exo means "from outside."
    These discoveries can spark a child's imagination about the infinite wonders of the universe.
    """
    
    Facts:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mYou are an expert fact checker. You have been hired by a major news organization to fact check a very important story.
    
    Here is a bullet point list of facts:
    """
    
    • The James Webb Space Telescope (JWST) spotted a number of galaxies nicknamed "green peas."
    • The telescope captured images of galaxies that are over 13 billion years old.
    • JWST took the very first pictures of a planet outside of our own solar system.
    • These distant worlds are called "exoplanets."
    """
    
    For each fact, determine whether it is true or false about the subject. If you are unable to determine whether the fact is true or false, output "Undetermined".
    If the fact is false, explain why.
    
    [0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true of false.  If the answer is false, a suggestion is given for a correction.
    
    Checked Assertions:
    """
    • The James Webb Space Telescope (JWST) spotted a number of galaxies nicknamed "green peas." - True 
    
    • The telescope captured images of galaxies that are over 13 billion years old. - True 
    
    • JWST took the very first pictures of a planet outside of our own solar system. - False. The first exoplanet was discovered in 1992, before the JWST was launched. 
    
    • These distant worlds are called "exoplanets." - True
    """
    
    Original Summary:
    """
    
    Your 9-year old might like these recent discoveries made by The James Webb Space Telescope (JWST):
    • In 2023, The JWST spotted a number of galaxies nicknamed "green peas." They were given this name because they are small, round, and green, like peas.
    • The telescope captured images of galaxies that are over 13 billion years old. This means that the light from these galaxies has been traveling for over 13 billion years to reach us.
    • JWST took the very first pictures of a planet outside of our own solar system. These distant worlds are called "exoplanets." Exo means "from outside."
    These discoveries can spark a child's imagination about the infinite wonders of the universe.
    """
    
    Using these checked assertions, rewrite the original summary to be completely true.
    
    The output should have the same structure and formatting as the original summary.
    
    Summary:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true or false.
    
    If all of the assertions are true, return "True". If any of the assertions are false, return "False".
    
    Here are some examples:
    ===
    
    Checked Assertions: """
    - The sky is red: False
    - Water is made of lava: False
    - The sun is a star: True
    """
    Result: False
    
    ===
    
    Checked Assertions: """
    - The sky is blue: True
    - Water is wet: True
    - The sun is a star: True
    """
    Result: True
    
    ===
    
    Checked Assertions: """
    - The sky is blue - True
    - Water is made of lava- False
    - The sun is a star - True
    """
    Result: False
    
    ===
    
    Checked Assertions:"""
    • The James Webb Space Telescope (JWST) spotted a number of galaxies nicknamed "green peas." - True 
    
    • The telescope captured images of galaxies that are over 13 billion years old. - True 
    
    • JWST took the very first pictures of a planet outside of our own solar system. - False. The first exoplanet was discovered in 1992, before the JWST was launched. 
    
    • These distant worlds are called "exoplanets." - True
    """
    Result:[0m
    
    [1m> Finished chain.[0m
    
    [1m> Finished chain.[0m
    
    
    Your 9-year old might like these recent discoveries made by The James Webb Space Telescope (JWST):
    • In 2023, The JWST spotted a number of galaxies nicknamed "green peas." They were given this name because they are small, round, and green, like peas.
    • The telescope captured images of galaxies that are over 13 billion years old. This means that the light from these galaxies has been traveling for over 13 billion years to reach us.
    • JWST has provided us with the first images of exoplanets, which are planets outside of our own solar system. These distant worlds were first discovered in 1992, and the JWST has allowed us to see them in greater detail.
    These discoveries can spark a child's imagination about the infinite wonders of the universe.
    
    
    [1m> Entering new SequentialChain chain...[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mGiven some text, extract a list of facts from the text.
    
    Format your output as a bulleted list.
    
    Text:
    """
    
    
    Your 9-year old might like these recent discoveries made by The James Webb Space Telescope (JWST):
    • In 2023, The JWST spotted a number of galaxies nicknamed "green peas." They were given this name because they are small, round, and green, like peas.
    • The telescope captured images of galaxies that are over 13 billion years old. This means that the light from these galaxies has been traveling for over 13 billion years to reach us.
    • JWST has provided us with the first images of exoplanets, which are planets outside of our own solar system. These distant worlds were first discovered in 1992, and the JWST has allowed us to see them in greater detail.
    These discoveries can spark a child's imagination about the infinite wonders of the universe.
    """
    
    Facts:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mYou are an expert fact checker. You have been hired by a major news organization to fact check a very important story.
    
    Here is a bullet point list of facts:
    """
    
    • The James Webb Space Telescope (JWST) spotted a number of galaxies nicknamed "green peas."
    • The light from these galaxies has been traveling for over 13 billion years to reach us.
    • JWST has provided us with the first images of exoplanets, which are planets outside of our own solar system.
    • Exoplanets were first discovered in 1992.
    • The JWST has allowed us to see exoplanets in greater detail.
    """
    
    For each fact, determine whether it is true or false about the subject. If you are unable to determine whether the fact is true or false, output "Undetermined".
    If the fact is false, explain why.
    
    [0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true of false.  If the answer is false, a suggestion is given for a correction.
    
    Checked Assertions:
    """
    
    • The James Webb Space Telescope (JWST) spotted a number of galaxies nicknamed "green peas." - True 
    
    • The light from these galaxies has been traveling for over 13 billion years to reach us. - True 
    
    • JWST has provided us with the first images of exoplanets, which are planets outside of our own solar system. - False. The first exoplanet was discovered in 1992, but the first images of exoplanets were taken by the Hubble Space Telescope in 2004. 
    
    • Exoplanets were first discovered in 1992. - True 
    
    • The JWST has allowed us to see exoplanets in greater detail. - Undetermined. The JWST has not yet been launched, so it is not yet known how much detail it will be able to provide.
    """
    
    Original Summary:
    """
    
    
    Your 9-year old might like these recent discoveries made by The James Webb Space Telescope (JWST):
    • In 2023, The JWST spotted a number of galaxies nicknamed "green peas." They were given this name because they are small, round, and green, like peas.
    • The telescope captured images of galaxies that are over 13 billion years old. This means that the light from these galaxies has been traveling for over 13 billion years to reach us.
    • JWST has provided us with the first images of exoplanets, which are planets outside of our own solar system. These distant worlds were first discovered in 1992, and the JWST has allowed us to see them in greater detail.
    These discoveries can spark a child's imagination about the infinite wonders of the universe.
    """
    
    Using these checked assertions, rewrite the original summary to be completely true.
    
    The output should have the same structure and formatting as the original summary.
    
    Summary:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true or false.
    
    If all of the assertions are true, return "True". If any of the assertions are false, return "False".
    
    Here are some examples:
    ===
    
    Checked Assertions: """
    - The sky is red: False
    - Water is made of lava: False
    - The sun is a star: True
    """
    Result: False
    
    ===
    
    Checked Assertions: """
    - The sky is blue: True
    - Water is wet: True
    - The sun is a star: True
    """
    Result: True
    
    ===
    
    Checked Assertions: """
    - The sky is blue - True
    - Water is made of lava- False
    - The sun is a star - True
    """
    Result: False
    
    ===
    
    Checked Assertions:"""
    
    • The James Webb Space Telescope (JWST) spotted a number of galaxies nicknamed "green peas." - True 
    
    • The light from these galaxies has been traveling for over 13 billion years to reach us. - True 
    
    • JWST has provided us with the first images of exoplanets, which are planets outside of our own solar system. - False. The first exoplanet was discovered in 1992, but the first images of exoplanets were taken by the Hubble Space Telescope in 2004. 
    
    • Exoplanets were first discovered in 1992. - True 
    
    • The JWST has allowed us to see exoplanets in greater detail. - Undetermined. The JWST has not yet been launched, so it is not yet known how much detail it will be able to provide.
    """
    Result:[0m
    
    [1m> Finished chain.[0m
    
    [1m> Finished chain.[0m
    
    
    Your 9-year old might like these recent discoveries made by The James Webb Space Telescope (JWST):
    • In 2023, The JWST will spot a number of galaxies nicknamed "green peas." They were given this name because they are small, round, and green, like peas.
    • The telescope will capture images of galaxies that are over 13 billion years old. This means that the light from these galaxies has been traveling for over 13 billion years to reach us.
    • Exoplanets, which are planets outside of our own solar system, were first discovered in 1992. The JWST will allow us to see them in greater detail when it is launched in 2023.
    These discoveries can spark a child's imagination about the infinite wonders of the universe.
    
    [1m> Finished chain.[0m
    




    'Your 9-year old might like these recent discoveries made by The James Webb Space Telescope (JWST):\n• In 2023, The JWST will spot a number of galaxies nicknamed "green peas." They were given this name because they are small, round, and green, like peas.\n• The telescope will capture images of galaxies that are over 13 billion years old. This means that the light from these galaxies has been traveling for over 13 billion years to reach us.\n• Exoplanets, which are planets outside of our own solar system, were first discovered in 1992. The JWST will allow us to see them in greater detail when it is launched in 2023.\nThese discoveries can spark a child\'s imagination about the infinite wonders of the universe.'




```python
from langchain.chains import LLMSummarizationCheckerChain
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)
checker_chain = LLMSummarizationCheckerChain.from_llm(llm, verbose=True, max_checks=3)
text = "The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. It has an area of 465,000 square miles and is one of five oceans in the world, alongside the Pacific Ocean, Atlantic Ocean, Indian Ocean, and the Southern Ocean. It is the smallest of the five oceans and is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. The sea is named after the island of Greenland, and is the Arctic Ocean's main outlet to the Atlantic. It is often frozen over so navigation is limited, and is considered the northern branch of the Norwegian Sea."
checker_chain.run(text)
```

    
    
    [1m> Entering new LLMSummarizationCheckerChain chain...[0m
    
    
    [1m> Entering new SequentialChain chain...[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mGiven some text, extract a list of facts from the text.
    
    Format your output as a bulleted list.
    
    Text:
    """
    The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. It has an area of 465,000 square miles and is one of five oceans in the world, alongside the Pacific Ocean, Atlantic Ocean, Indian Ocean, and the Southern Ocean. It is the smallest of the five oceans and is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. The sea is named after the island of Greenland, and is the Arctic Ocean's main outlet to the Atlantic. It is often frozen over so navigation is limited, and is considered the northern branch of the Norwegian Sea.
    """
    
    Facts:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mYou are an expert fact checker. You have been hired by a major news organization to fact check a very important story.
    
    Here is a bullet point list of facts:
    """
    
    - The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland.
    - It has an area of 465,000 square miles.
    - It is one of five oceans in the world, alongside the Pacific Ocean, Atlantic Ocean, Indian Ocean, and the Southern Ocean.
    - It is the smallest of the five oceans.
    - It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs.
    - The sea is named after the island of Greenland.
    - It is the Arctic Ocean's main outlet to the Atlantic.
    - It is often frozen over so navigation is limited.
    - It is considered the northern branch of the Norwegian Sea.
    """
    
    For each fact, determine whether it is true or false about the subject. If you are unable to determine whether the fact is true or false, output "Undetermined".
    If the fact is false, explain why.
    
    [0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true of false.  If the answer is false, a suggestion is given for a correction.
    
    Checked Assertions:
    """
    
    - The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. True
    
    - It has an area of 465,000 square miles. True
    
    - It is one of five oceans in the world, alongside the Pacific Ocean, Atlantic Ocean, Indian Ocean, and the Southern Ocean. False - The Greenland Sea is not an ocean, it is an arm of the Arctic Ocean.
    
    - It is the smallest of the five oceans. False - The Greenland Sea is not an ocean, it is an arm of the Arctic Ocean.
    
    - It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. True
    
    - The sea is named after the island of Greenland. True
    
    - It is the Arctic Ocean's main outlet to the Atlantic. True
    
    - It is often frozen over so navigation is limited. True
    
    - It is considered the northern branch of the Norwegian Sea. True
    """
    
    Original Summary:
    """
    The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. It has an area of 465,000 square miles and is one of five oceans in the world, alongside the Pacific Ocean, Atlantic Ocean, Indian Ocean, and the Southern Ocean. It is the smallest of the five oceans and is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. The sea is named after the island of Greenland, and is the Arctic Ocean's main outlet to the Atlantic. It is often frozen over so navigation is limited, and is considered the northern branch of the Norwegian Sea.
    """
    
    Using these checked assertions, rewrite the original summary to be completely true.
    
    The output should have the same structure and formatting as the original summary.
    
    Summary:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true or false.
    
    If all of the assertions are true, return "True". If any of the assertions are false, return "False".
    
    Here are some examples:
    ===
    
    Checked Assertions: """
    - The sky is red: False
    - Water is made of lava: False
    - The sun is a star: True
    """
    Result: False
    
    ===
    
    Checked Assertions: """
    - The sky is blue: True
    - Water is wet: True
    - The sun is a star: True
    """
    Result: True
    
    ===
    
    Checked Assertions: """
    - The sky is blue - True
    - Water is made of lava- False
    - The sun is a star - True
    """
    Result: False
    
    ===
    
    Checked Assertions:"""
    
    - The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. True
    
    - It has an area of 465,000 square miles. True
    
    - It is one of five oceans in the world, alongside the Pacific Ocean, Atlantic Ocean, Indian Ocean, and the Southern Ocean. False - The Greenland Sea is not an ocean, it is an arm of the Arctic Ocean.
    
    - It is the smallest of the five oceans. False - The Greenland Sea is not an ocean, it is an arm of the Arctic Ocean.
    
    - It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. True
    
    - The sea is named after the island of Greenland. True
    
    - It is the Arctic Ocean's main outlet to the Atlantic. True
    
    - It is often frozen over so navigation is limited. True
    
    - It is considered the northern branch of the Norwegian Sea. True
    """
    Result:[0m
    
    [1m> Finished chain.[0m
    
    [1m> Finished chain.[0m
    
    The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. It has an area of 465,000 square miles and is an arm of the Arctic Ocean. It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. The sea is named after the island of Greenland, and is the Arctic Ocean's main outlet to the Atlantic. It is often frozen over so navigation is limited, and is considered the northern branch of the Norwegian Sea.
    
    
    [1m> Entering new SequentialChain chain...[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mGiven some text, extract a list of facts from the text.
    
    Format your output as a bulleted list.
    
    Text:
    """
    
    The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. It has an area of 465,000 square miles and is an arm of the Arctic Ocean. It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. The sea is named after the island of Greenland, and is the Arctic Ocean's main outlet to the Atlantic. It is often frozen over so navigation is limited, and is considered the northern branch of the Norwegian Sea.
    """
    
    Facts:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mYou are an expert fact checker. You have been hired by a major news organization to fact check a very important story.
    
    Here is a bullet point list of facts:
    """
    
    - The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland.
    - It has an area of 465,000 square miles.
    - It is an arm of the Arctic Ocean.
    - It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs.
    - It is named after the island of Greenland.
    - It is the Arctic Ocean's main outlet to the Atlantic.
    - It is often frozen over so navigation is limited.
    - It is considered the northern branch of the Norwegian Sea.
    """
    
    For each fact, determine whether it is true or false about the subject. If you are unable to determine whether the fact is true or false, output "Undetermined".
    If the fact is false, explain why.
    
    [0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true of false.  If the answer is false, a suggestion is given for a correction.
    
    Checked Assertions:
    """
    
    - The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. True
    
    - It has an area of 465,000 square miles. True
    
    - It is an arm of the Arctic Ocean. True
    
    - It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. True
    
    - It is named after the island of Greenland. False - It is named after the country of Greenland.
    
    - It is the Arctic Ocean's main outlet to the Atlantic. True
    
    - It is often frozen over so navigation is limited. True
    
    - It is considered the northern branch of the Norwegian Sea. False - It is considered the northern branch of the Atlantic Ocean.
    """
    
    Original Summary:
    """
    
    The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. It has an area of 465,000 square miles and is an arm of the Arctic Ocean. It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. The sea is named after the island of Greenland, and is the Arctic Ocean's main outlet to the Atlantic. It is often frozen over so navigation is limited, and is considered the northern branch of the Norwegian Sea.
    """
    
    Using these checked assertions, rewrite the original summary to be completely true.
    
    The output should have the same structure and formatting as the original summary.
    
    Summary:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true or false.
    
    If all of the assertions are true, return "True". If any of the assertions are false, return "False".
    
    Here are some examples:
    ===
    
    Checked Assertions: """
    - The sky is red: False
    - Water is made of lava: False
    - The sun is a star: True
    """
    Result: False
    
    ===
    
    Checked Assertions: """
    - The sky is blue: True
    - Water is wet: True
    - The sun is a star: True
    """
    Result: True
    
    ===
    
    Checked Assertions: """
    - The sky is blue - True
    - Water is made of lava- False
    - The sun is a star - True
    """
    Result: False
    
    ===
    
    Checked Assertions:"""
    
    - The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. True
    
    - It has an area of 465,000 square miles. True
    
    - It is an arm of the Arctic Ocean. True
    
    - It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. True
    
    - It is named after the island of Greenland. False - It is named after the country of Greenland.
    
    - It is the Arctic Ocean's main outlet to the Atlantic. True
    
    - It is often frozen over so navigation is limited. True
    
    - It is considered the northern branch of the Norwegian Sea. False - It is considered the northern branch of the Atlantic Ocean.
    """
    Result:[0m
    
    [1m> Finished chain.[0m
    
    [1m> Finished chain.[0m
    
    
    The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. It has an area of 465,000 square miles and is an arm of the Arctic Ocean. It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. The sea is named after the country of Greenland, and is the Arctic Ocean's main outlet to the Atlantic. It is often frozen over so navigation is limited, and is considered the northern branch of the Atlantic Ocean.
    
    
    [1m> Entering new SequentialChain chain...[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mGiven some text, extract a list of facts from the text.
    
    Format your output as a bulleted list.
    
    Text:
    """
    
    
    The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. It has an area of 465,000 square miles and is an arm of the Arctic Ocean. It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. The sea is named after the country of Greenland, and is the Arctic Ocean's main outlet to the Atlantic. It is often frozen over so navigation is limited, and is considered the northern branch of the Atlantic Ocean.
    """
    
    Facts:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mYou are an expert fact checker. You have been hired by a major news organization to fact check a very important story.
    
    Here is a bullet point list of facts:
    """
    
    - The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland.
    - It has an area of 465,000 square miles.
    - It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs.
    - The sea is named after the country of Greenland.
    - It is the Arctic Ocean's main outlet to the Atlantic.
    - It is often frozen over so navigation is limited.
    - It is considered the northern branch of the Atlantic Ocean.
    """
    
    For each fact, determine whether it is true or false about the subject. If you are unable to determine whether the fact is true or false, output "Undetermined".
    If the fact is false, explain why.
    
    [0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true of false.  If the answer is false, a suggestion is given for a correction.
    
    Checked Assertions:
    """
    
    - The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. True
    
    - It has an area of 465,000 square miles. True
    
    - It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. True
    
    - The sea is named after the country of Greenland. True
    
    - It is the Arctic Ocean's main outlet to the Atlantic. False - The Arctic Ocean's main outlet to the Atlantic is the Barents Sea.
    
    - It is often frozen over so navigation is limited. True
    
    - It is considered the northern branch of the Atlantic Ocean. False - The Greenland Sea is considered part of the Arctic Ocean, not the Atlantic Ocean.
    """
    
    Original Summary:
    """
    
    
    The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. It has an area of 465,000 square miles and is an arm of the Arctic Ocean. It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. The sea is named after the country of Greenland, and is the Arctic Ocean's main outlet to the Atlantic. It is often frozen over so navigation is limited, and is considered the northern branch of the Atlantic Ocean.
    """
    
    Using these checked assertions, rewrite the original summary to be completely true.
    
    The output should have the same structure and formatting as the original summary.
    
    Summary:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true or false.
    
    If all of the assertions are true, return "True". If any of the assertions are false, return "False".
    
    Here are some examples:
    ===
    
    Checked Assertions: """
    - The sky is red: False
    - Water is made of lava: False
    - The sun is a star: True
    """
    Result: False
    
    ===
    
    Checked Assertions: """
    - The sky is blue: True
    - Water is wet: True
    - The sun is a star: True
    """
    Result: True
    
    ===
    
    Checked Assertions: """
    - The sky is blue - True
    - Water is made of lava- False
    - The sun is a star - True
    """
    Result: False
    
    ===
    
    Checked Assertions:"""
    
    - The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. True
    
    - It has an area of 465,000 square miles. True
    
    - It is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. True
    
    - The sea is named after the country of Greenland. True
    
    - It is the Arctic Ocean's main outlet to the Atlantic. False - The Arctic Ocean's main outlet to the Atlantic is the Barents Sea.
    
    - It is often frozen over so navigation is limited. True
    
    - It is considered the northern branch of the Atlantic Ocean. False - The Greenland Sea is considered part of the Arctic Ocean, not the Atlantic Ocean.
    """
    Result:[0m
    
    [1m> Finished chain.[0m
    
    [1m> Finished chain.[0m
    
    
    The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. It has an area of 465,000 square miles and is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. The sea is named after the country of Greenland, and is the Arctic Ocean's main outlet to the Barents Sea. It is often frozen over so navigation is limited, and is considered part of the Arctic Ocean.
    
    [1m> Finished chain.[0m
    




    "The Greenland Sea is an outlying portion of the Arctic Ocean located between Iceland, Norway, the Svalbard archipelago and Greenland. It has an area of 465,000 square miles and is covered almost entirely by water, some of which is frozen in the form of glaciers and icebergs. The sea is named after the country of Greenland, and is the Arctic Ocean's main outlet to the Barents Sea. It is often frozen over so navigation is limited, and is considered part of the Arctic Ocean."




```python
from langchain.chains import LLMSummarizationCheckerChain
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)
checker_chain = LLMSummarizationCheckerChain.from_llm(llm, max_checks=3, verbose=True)
text = "Mammals can lay eggs, birds can lay eggs, therefore birds are mammals."
checker_chain.run(text)
```

    
    
    [1m> Entering new LLMSummarizationCheckerChain chain...[0m
    
    
    [1m> Entering new SequentialChain chain...[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mGiven some text, extract a list of facts from the text.
    
    Format your output as a bulleted list.
    
    Text:
    """
    Mammals can lay eggs, birds can lay eggs, therefore birds are mammals.
    """
    
    Facts:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mYou are an expert fact checker. You have been hired by a major news organization to fact check a very important story.
    
    Here is a bullet point list of facts:
    """
    
    - Mammals can lay eggs
    - Birds can lay eggs
    - Birds are mammals
    """
    
    For each fact, determine whether it is true or false about the subject. If you are unable to determine whether the fact is true or false, output "Undetermined".
    If the fact is false, explain why.
    
    [0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true of false.  If the answer is false, a suggestion is given for a correction.
    
    Checked Assertions:
    """
    
    - Mammals can lay eggs: False. Mammals are not capable of laying eggs, as they give birth to live young.
    
    - Birds can lay eggs: True. Birds are capable of laying eggs.
    
    - Birds are mammals: False. Birds are not mammals, they are a class of their own.
    """
    
    Original Summary:
    """
    Mammals can lay eggs, birds can lay eggs, therefore birds are mammals.
    """
    
    Using these checked assertions, rewrite the original summary to be completely true.
    
    The output should have the same structure and formatting as the original summary.
    
    Summary:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true or false.
    
    If all of the assertions are true, return "True". If any of the assertions are false, return "False".
    
    Here are some examples:
    ===
    
    Checked Assertions: """
    - The sky is red: False
    - Water is made of lava: False
    - The sun is a star: True
    """
    Result: False
    
    ===
    
    Checked Assertions: """
    - The sky is blue: True
    - Water is wet: True
    - The sun is a star: True
    """
    Result: True
    
    ===
    
    Checked Assertions: """
    - The sky is blue - True
    - Water is made of lava- False
    - The sun is a star - True
    """
    Result: False
    
    ===
    
    Checked Assertions:"""
    
    - Mammals can lay eggs: False. Mammals are not capable of laying eggs, as they give birth to live young.
    
    - Birds can lay eggs: True. Birds are capable of laying eggs.
    
    - Birds are mammals: False. Birds are not mammals, they are a class of their own.
    """
    Result:[0m
    
    [1m> Finished chain.[0m
    
    [1m> Finished chain.[0m
     Birds and mammals are both capable of laying eggs, however birds are not mammals, they are a class of their own.
    
    
    [1m> Entering new SequentialChain chain...[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mGiven some text, extract a list of facts from the text.
    
    Format your output as a bulleted list.
    
    Text:
    """
     Birds and mammals are both capable of laying eggs, however birds are not mammals, they are a class of their own.
    """
    
    Facts:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mYou are an expert fact checker. You have been hired by a major news organization to fact check a very important story.
    
    Here is a bullet point list of facts:
    """
    
    - Birds and mammals are both capable of laying eggs.
    - Birds are not mammals.
    - Birds are a class of their own.
    """
    
    For each fact, determine whether it is true or false about the subject. If you are unable to determine whether the fact is true or false, output "Undetermined".
    If the fact is false, explain why.
    
    [0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true of false.  If the answer is false, a suggestion is given for a correction.
    
    Checked Assertions:
    """
    
    - Birds and mammals are both capable of laying eggs: False. Mammals give birth to live young, while birds lay eggs.
    
    - Birds are not mammals: True. Birds are a class of their own, separate from mammals.
    
    - Birds are a class of their own: True. Birds are a class of their own, separate from mammals.
    """
    
    Original Summary:
    """
     Birds and mammals are both capable of laying eggs, however birds are not mammals, they are a class of their own.
    """
    
    Using these checked assertions, rewrite the original summary to be completely true.
    
    The output should have the same structure and formatting as the original summary.
    
    Summary:[0m
    
    [1m> Finished chain.[0m
    
    
    [1m> Entering new LLMChain chain...[0m
    Prompt after formatting:
    [32;1m[1;3mBelow are some assertions that have been fact checked and are labeled as true or false.
    
    If all of the assertions are true, return "True". If any of the assertions are false, return "False".
    
    Here are some examples:
    ===
    
    Checked Assertions: """
    - The sky is red: False
    - Water is made of lava: False
    - The sun is a star: True
    """
    Result: False
    
    ===
    
    Checked Assertions: """
    - The sky is blue: True
    - Water is wet: True
    - The sun is a star: True
    """
    Result: True
    
    ===
    
    Checked Assertions: """
    - The sky is blue - True
    - Water is made of lava- False
    - The sun is a star - True
    """
    Result: False
    
    ===
    
    Checked Assertions:"""
    
    - Birds and mammals are both capable of laying eggs: False. Mammals give birth to live young, while birds lay eggs.
    
    - Birds are not mammals: True. Birds are a class of their own, separate from mammals.
    
    - Birds are a class of their own: True. Birds are a class of their own, separate from mammals.
    """
    Result:[0m
    
    [1m> Finished chain.[0m
    
    [1m> Finished chain.[0m
    
    [1m> Finished chain.[0m
    




    'Birds are not mammals, but they are a class of their own. They lay eggs, unlike mammals which give birth to live young.'


