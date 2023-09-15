# Docugami
This notebook covers how to load documents from `Docugami`. It provides the advantages of using this system over alternative data loaders.

## Prerequisites
1. Install necessary python packages.
2. Grab an access token for your workspace, and make sure it is set as the `DOCUGAMI_API_KEY` environment variable.
3. Grab some docset and document IDs for your processed documents, as described here: https://help.docugami.com/home/docugami-api


```python
# You need the lxml package to use the DocugamiLoader
!pip install lxml
```

## Quick start

1. Create a [Docugami workspace](http://www.docugami.com) (free trials available)
2. Add your documents (PDF, DOCX or DOC) and allow Docugami to ingest and cluster them into sets of similar documents, e.g. NDAs, Lease Agreements, and Service Agreements. There is no fixed set of document types supported by the system, the clusters created depend on your particular documents, and you can [change the docset assignments](https://help.docugami.com/home/working-with-the-doc-sets-view) later.
3. Create an access token via the Developer Playground for your workspace. [Detailed instructions](https://help.docugami.com/home/docugami-api)
4. Explore the [Docugami API](https://api-docs.docugami.com) to get a list of your processed docset IDs, or just the document IDs for a particular docset. 
6. Use the DocugamiLoader as detailed below, to get rich semantic chunks for your documents.
7. Optionally, build and publish one or more [reports or abstracts](https://help.docugami.com/home/reports). This helps Docugami improve the semantic XML with better tags based on your preferences, which are then added to the DocugamiLoader output as metadata. Use techniques like [self-querying retriever](https://python.langchain.com/en/latest/modules/data_connection/retrievers/examples/self_query_retriever.html) to do high accuracy Document QA.

## Advantages vs Other Chunking Techniques

Appropriate chunking of your documents is critical for retrieval from documents. Many chunking techniques exist, including simple ones that rely on whitespace and recursive chunk splitting based on character length. Docugami offers a different approach:

1. **Intelligent Chunking:** Docugami breaks down every document into a hierarchical semantic XML tree of chunks of varying sizes, from single words or numerical values to entire sections. These chunks follow the semantic contours of the document, providing a more meaningful representation than arbitrary length or simple whitespace-based chunking.
2. **Structured Representation:** In addition, the XML tree indicates the structural contours of every document, using attributes denoting headings, paragraphs, lists, tables, and other common elements, and does that consistently across all supported document formats, such as scanned PDFs or DOCX files. It appropriately handles long-form document characteristics like page headers/footers or multi-column flows for clean text extraction.
3. **Semantic Annotations:** Chunks are annotated with semantic tags that are coherent across the document set, facilitating consistent hierarchical queries across multiple documents, even if they are written and formatted differently. For example, in set of lease agreements, you can easily identify key provisions like the Landlord, Tenant, or Renewal Date, as well as more complex information such as the wording of any sub-lease provision or whether a specific jurisdiction has an exception section within a Termination Clause.
4. **Additional Metadata:** Chunks are also annotated with additional metadata, if a user has been using Docugami. This additional metadata can be used for high-accuracy Document QA without context window restrictions. See detailed code walk-through below.



```python
import os
from langchain.document_loaders import DocugamiLoader
```

## Load Documents

If the DOCUGAMI_API_KEY environment variable is set, there is no need to pass it in to the loader explicitly otherwise you can pass it in as the `access_token` parameter.


```python
DOCUGAMI_API_KEY = os.environ.get("DOCUGAMI_API_KEY")

# To load all docs in the given docset ID, just don't provide document_ids
loader = DocugamiLoader(docset_id="ecxqpipcoe2p", document_ids=["43rj0ds7s0ur"])
docs = loader.load()
docs
```




    [Document(page_content='MUTUAL NON-DISCLOSURE AGREEMENT This  Mutual Non-Disclosure Agreement  (this “ Agreement ”) is entered into and made effective as of  April  4 ,  2018  between  Docugami Inc. , a  Delaware  corporation , whose address is  150  Lake Street South ,  Suite  221 ,  Kirkland ,  Washington  98033 , and  Caleb Divine , an individual, whose address is  1201  Rt  300 ,  Newburgh  NY  12550 .', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:ThisMutualNon-disclosureAgreement', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'p', 'tag': 'ThisMutualNon-disclosureAgreement'}),
     Document(page_content='The above named parties desire to engage in discussions regarding a potential agreement or other transaction between the parties (the “Purpose”). In connection with such discussions, it may be necessary for the parties to disclose to each other certain confidential information or materials to enable them to evaluate whether to enter into such agreement or transaction.', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Discussions', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'p', 'tag': 'Discussions'}),
     Document(page_content='In consideration of the foregoing, the parties agree as follows:', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Consideration', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'p', 'tag': 'Consideration'}),
     Document(page_content='1. Confidential Information . For purposes of this  Agreement , “ Confidential Information ” means any information or materials disclosed by  one  party  to the other party that: (i) if disclosed in writing or in the form of tangible materials, is marked “confidential” or “proprietary” at the time of such disclosure; (ii) if disclosed orally or by visual presentation, is identified as “confidential” or “proprietary” at the time of such disclosure, and is summarized in a writing sent by the disclosing party to the receiving party within  thirty  ( 30 ) days  after any such disclosure; or (iii) due to its nature or the circumstances of its disclosure, a person exercising reasonable business judgment would understand to be confidential or proprietary.', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:Purposes/docset:ConfidentialInformation-section/docset:ConfidentialInformation[2]', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'div', 'tag': 'ConfidentialInformation'}),
     Document(page_content="2. Obligations and  Restrictions . Each party agrees: (i) to maintain the  other party's Confidential Information  in strict confidence; (ii) not to disclose  such Confidential Information  to any third party; and (iii) not to use  such Confidential Information  for any purpose except for the Purpose. Each party may disclose the  other party’s Confidential Information  to its employees and consultants who have a bona fide need to know  such Confidential Information  for the Purpose, but solely to the extent necessary to pursue the  Purpose  and for no other purpose; provided, that each such employee and consultant first executes a written agreement (or is otherwise already bound by a written agreement) that contains use and nondisclosure restrictions at least as protective of the  other party’s Confidential Information  as those set forth in this  Agreement .", metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:Obligations/docset:ObligationsAndRestrictions-section/docset:ObligationsAndRestrictions', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'div', 'tag': 'ObligationsAndRestrictions'}),
     Document(page_content='3. Exceptions. The obligations and restrictions in Section  2  will not apply to any information or materials that:', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:Exceptions/docset:Exceptions-section/docset:Exceptions[2]', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'div', 'tag': 'Exceptions'}),
     Document(page_content='(i) were, at the date of disclosure, or have subsequently become, generally known or available to the public through no act or failure to act by the receiving party;', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:TheDate/docset:TheDate/docset:TheDate', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'p', 'tag': 'TheDate'}),
     Document(page_content='(ii) were rightfully known by the receiving party prior to receiving such information or materials from the disclosing party;', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:TheDate/docset:SuchInformation/docset:TheReceivingParty', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'p', 'tag': 'TheReceivingParty'}),
     Document(page_content='(iii) are rightfully acquired by the receiving party from a third party who has the right to disclose such information or materials without breach of any confidentiality obligation to the disclosing party;', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:TheDate/docset:TheReceivingParty/docset:TheReceivingParty', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'p', 'tag': 'TheReceivingParty'}),
     Document(page_content='4. Compelled Disclosure . Nothing in this  Agreement  will be deemed to restrict a party from disclosing the  other party’s Confidential Information  to the extent required by any order, subpoena, law, statute or regulation; provided, that the party required to make such a disclosure uses reasonable efforts to give the other party reasonable advance notice of such required disclosure in order to enable the other party to prevent or limit such disclosure.', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:Disclosure/docset:CompelledDisclosure-section/docset:CompelledDisclosure', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'div', 'tag': 'CompelledDisclosure'}),
     Document(page_content='5. Return of  Confidential Information . Upon the completion or abandonment of the Purpose, and in any event upon the disclosing party’s request, the receiving party will promptly return to the disclosing party all tangible items and embodiments containing or consisting of the  disclosing party’s Confidential Information  and all copies thereof (including electronic copies), and any notes, analyses, compilations, studies, interpretations, memoranda or other documents (regardless of the form thereof) prepared by or on behalf of the receiving party that contain or are based upon the  disclosing party’s Confidential Information .', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:TheCompletion/docset:ReturnofConfidentialInformation-section/docset:ReturnofConfidentialInformation', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'div', 'tag': 'ReturnofConfidentialInformation'}),
     Document(page_content='6. No  Obligations . Each party retains the right to determine whether to disclose any  Confidential Information  to the other party.', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:NoObligations/docset:NoObligations-section/docset:NoObligations[2]', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'div', 'tag': 'NoObligations'}),
     Document(page_content='7. No Warranty. ALL  CONFIDENTIAL INFORMATION  IS PROVIDED BY THE  DISCLOSING PARTY  “AS  IS ”.', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:NoWarranty/docset:NoWarranty-section/docset:NoWarranty[2]', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'div', 'tag': 'NoWarranty'}),
     Document(page_content='8. Term. This  Agreement  will remain in effect for a period of  seven  ( 7 ) years  from the date of last disclosure of  Confidential Information  by either party, at which time it will terminate.', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:ThisAgreement/docset:Term-section/docset:Term', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'div', 'tag': 'Term'}),
     Document(page_content='9. Equitable Relief . Each party acknowledges that the unauthorized use or disclosure of the  disclosing party’s Confidential Information  may cause the disclosing party to incur irreparable harm and significant damages, the degree of which may be difficult to ascertain. Accordingly, each party agrees that the disclosing party will have the right to seek immediate equitable relief to enjoin any unauthorized use or disclosure of  its Confidential Information , in addition to any other rights and remedies that it may have at law or otherwise.', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:EquitableRelief/docset:EquitableRelief-section/docset:EquitableRelief[2]', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'div', 'tag': 'EquitableRelief'}),
     Document(page_content='10. Non-compete. To the maximum extent permitted by applicable law, during the  Term  of this  Agreement  and for a period of  one  ( 1 ) year  thereafter,  Caleb  Divine  may not market software products or do business that directly or indirectly competes with  Docugami  software products .', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:TheMaximumExtent/docset:Non-compete-section/docset:Non-compete', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'div', 'tag': 'Non-compete'}),
     Document(page_content='11. Miscellaneous. This  Agreement  will be governed and construed in accordance with the laws of the  State  of  Washington , excluding its body of law controlling conflict of laws. This  Agreement  is the complete and exclusive understanding and agreement between the parties regarding the subject matter of this  Agreement  and supersedes all prior agreements, understandings and communications, oral or written, between the parties regarding the subject matter of this  Agreement . If any provision of this  Agreement  is held invalid or unenforceable by a court of competent jurisdiction, that provision of this  Agreement  will be enforced to the maximum extent permissible and the other provisions of this  Agreement  will remain in full force and effect. Neither party may assign this  Agreement , in whole or in part, by operation of law or otherwise, without the other party’s prior written consent, and any attempted assignment without such consent will be void. This  Agreement  may be executed in counterparts, each of which will be deemed an original, but all of which together will constitute one and the same instrument.', metadata={'xpath': '/docset:MutualNon-disclosure/docset:MutualNon-disclosure/docset:MUTUALNON-DISCLOSUREAGREEMENT-section/docset:MUTUALNON-DISCLOSUREAGREEMENT/docset:Consideration/docset:Purposes/docset:Accordance/docset:Miscellaneous-section/docset:Miscellaneous', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'div', 'tag': 'Miscellaneous'}),
     Document(page_content='[SIGNATURE PAGE FOLLOWS] IN  WITNESS  WHEREOF, the parties hereto have executed this  Mutual Non-Disclosure Agreement  by their duly authorized officers or representatives as of the date first set forth above.', metadata={'xpath': '/docset:MutualNon-disclosure/docset:Witness/docset:TheParties/docset:TheParties', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': 'p', 'tag': 'TheParties'}),
     Document(page_content='DOCUGAMI INC . : \n\n Caleb Divine : \n\n Signature:  Signature:  Name: \n\n Jean Paoli  Name:  Title: \n\n CEO  Title:', metadata={'xpath': '/docset:MutualNon-disclosure/docset:Witness/docset:TheParties/docset:DocugamiInc/docset:DocugamiInc/xhtml:table', 'id': '43rj0ds7s0ur', 'name': 'NDA simple layout.docx', 'structure': '', 'tag': 'table'})]



The `metadata` for each `Document` (really, a chunk of an actual PDF, DOC or DOCX) contains some useful additional information:

1. **id and name:** ID and Name of the file (PDF, DOC or DOCX) the chunk is sourced from within Docugami.
2. **xpath:** XPath inside the XML representation of the document, for the chunk. Useful for source citations directly to the actual chunk inside the document XML.
3. **structure:** Structural attributes of the chunk, e.g. h1, h2, div, table, td, etc. Useful to filter out certain kinds of chunks if needed by the caller.
4. **tag:** Semantic tag for the chunk, using various generative and extractive techniques. More details here: https://github.com/docugami/DFM-benchmarks

## Basic Use: Docugami Loader for Document QA

You can use the Docugami Loader like a standard loader for Document QA over multiple docs, albeit with much better chunks that follow the natural contours of the document. There are many great tutorials on how to do this, e.g. [this one](https://www.youtube.com/watch?v=3yPBVii7Ct0). We can just use the same code, but use the `DocugamiLoader` for better chunking, instead of loading text or PDF files directly with basic splitting techniques.


```python
!poetry run pip -q install openai tiktoken chromadb
```


```python
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# For this example, we already have a processed docset for a set of lease documents
loader = DocugamiLoader(docset_id="wh2kned25uqm")
documents = loader.load()
```

The documents returned by the loader are already split, so we don't need to use a text splitter. Optionally, we can use the metadata on each document, for example the structure or tag attributes, to do any post-processing we want.

We will just use the output of the `DocugamiLoader` as-is to set up a retrieval QA chain the usual way.


```python
embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents=documents, embedding=embedding)
retriever = vectordb.as_retriever()
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True
)
```

    Using embedded DuckDB without persistence: data will be transient
    


```python
# Try out the retriever with an example query
qa_chain("What can tenants do with signage on their properties?")
```




    {'query': 'What can tenants do with signage on their properties?',
     'result': ' Tenants may place signs (digital or otherwise) or other form of identification on the premises after receiving written permission from the landlord which shall not be unreasonably withheld. The tenant is responsible for any damage caused to the premises and must conform to any applicable laws, ordinances, etc. governing the same. The tenant must also remove and clean any window or glass identification promptly upon vacating the premises.',
     'source_documents': [Document(page_content='ARTICLE VI  SIGNAGE 6.01  Signage . Tenant  may place or attach to the  Premises signs  (digital or otherwise) or other such identification as needed after receiving written permission from the  Landlord , which permission shall not be unreasonably withheld. Any damage caused to the Premises by the  Tenant ’s erecting or removing such signs shall be repaired promptly by the  Tenant  at the  Tenant ’s expense . Any signs or other form of identification allowed must conform to all applicable laws, ordinances, etc. governing the same.  Tenant  also agrees to have any window or glass identification completely removed and cleaned at its expense promptly upon vacating the Premises.', metadata={'xpath': '/docset:OFFICELEASEAGREEMENT-section/docset:OFFICELEASEAGREEMENT/docset:Article/docset:ARTICLEVISIGNAGE-section/docset:_601Signage-section/docset:_601Signage', 'id': 'v1bvgaozfkak', 'name': 'TruTone Lane 2.docx', 'structure': 'div', 'tag': '_601Signage', 'Landlord': 'BUBBA CENTER PARTNERSHIP', 'Tenant': 'Truetone Lane LLC'}),
      Document(page_content='Signage.  Tenant  may place or attach to the  Premises signs  (digital or otherwise) or other such identification as needed after receiving written permission from the  Landlord , which permission shall not be unreasonably withheld. Any damage caused to the Premises by the  Tenant ’s erecting or removing such signs shall be repaired promptly by the  Tenant  at the  Tenant ’s expense . Any signs or other form of identification allowed must conform to all applicable laws, ordinances, etc. governing the same.  Tenant  also agrees to have any window or glass identification completely removed and cleaned at its expense promptly upon vacating the Premises. \n\n                                                          ARTICLE  VII  UTILITIES 7.01', metadata={'xpath': '/docset:OFFICELEASEAGREEMENT-section/docset:OFFICELEASEAGREEMENT/docset:ThisOFFICELEASEAGREEMENTThis/docset:ArticleIBasic/docset:ArticleIiiUseAndCareOf/docset:ARTICLEIIIUSEANDCAREOFPREMISES-section/docset:ARTICLEIIIUSEANDCAREOFPREMISES/docset:NoOtherPurposes/docset:TenantsResponsibility/dg:chunk', 'id': 'g2fvhekmltza', 'name': 'TruTone Lane 6.pdf', 'structure': 'lim', 'tag': 'chunk', 'Landlord': 'GLORY ROAD LLC', 'Tenant': 'Truetone Lane LLC'}),
      Document(page_content='Landlord , its agents, servants, employees, licensees, invitees, and contractors during the last year of the term of this  Lease  at any and all times during regular business hours, after  24  hour  notice  to tenant, to pass and repass on and through the Premises, or such portion thereof as may be necessary, in order that they or any of them may gain access to the Premises for the purpose of showing the  Premises  to potential new tenants or real estate brokers. In addition,  Landlord  shall be entitled to place a "FOR  RENT " or "FOR LEASE" sign (not exceeding  8.5 ” x  11 ”) in the front window of the Premises during the  last  six  months  of the term of this  Lease .', metadata={'xpath': '/docset:Rider/docset:RIDERTOLEASE-section/docset:RIDERTOLEASE/docset:FixedRent/docset:TermYearPeriod/docset:Lease/docset:_42FLandlordSAccess-section/docset:_42FLandlordSAccess/docset:LandlordsRights/docset:Landlord', 'id': 'omvs4mysdk6b', 'name': 'TruTone Lane 1.docx', 'structure': 'p', 'tag': 'Landlord', 'Landlord': 'BIRCH STREET ,  LLC', 'Tenant': 'Trutone Lane LLC'}),
      Document(page_content="24. SIGNS . No signage shall be placed by  Tenant  on any portion of the  Project . However,  Tenant  shall be permitted to place a sign bearing its name in a location approved by  Landlord  near the entrance to the  Premises  (at  Tenant's cost ) and will be furnished a single listing of its name in the  Building's directory  (at  Landlord 's cost ), all in accordance with the criteria adopted  from time to time  by  Landlord  for the  Project . Any changes or additional listings in the directory shall be furnished (subject to availability of space) for the  then Building Standard charge .", metadata={'xpath': '/docset:OFFICELEASE-section/docset:OFFICELEASE/docset:THISOFFICELEASE/docset:WITNESSETH-section/docset:WITNESSETH/docset:GrossRentCreditTheRentCredit-section/docset:GrossRentCreditTheRentCredit/docset:Period/docset:ApplicableSalesTax/docset:PercentageRent/docset:TheTerms/docset:Indemnification/docset:INDEMNIFICATION-section/docset:INDEMNIFICATION/docset:Waiver/docset:Waiver/docset:Signs/docset:SIGNS-section/docset:SIGNS', 'id': 'qkn9cyqsiuch', 'name': 'Shorebucks LLC_AZ.pdf', 'structure': 'div', 'tag': 'SIGNS', 'Landlord': 'Menlo Group', 'Tenant': 'Shorebucks LLC'})]}



## Using Docugami to Add Metadata to Chunks for High Accuracy Document QA

One issue with large documents is that the correct answer to your question may depend on chunks that are far apart in the document. Typical chunking techniques, even with overlap, will struggle with providing the LLM sufficent context to answer such questions. With upcoming very large context LLMs, it may be possible to stuff a lot of tokens, perhaps even entire documents, inside the context but this will still hit limits at some point with very long documents, or a lot of documents.

For example, if we ask a more complex question that requires the LLM to draw on chunks from different parts of the document, even OpenAI's powerful LLM is unable to answer correctly.


```python
chain_response = qa_chain("What is rentable area for the property owned by DHA Group?")
chain_response["result"]  # the correct answer should be 13,500
```




    ' 9,753 square feet'



At first glance the answer may seem reasonable, but if you review the source chunks carefully for this answer, you will see that the chunking of the document did not end up putting the Landlord name and the rentable area in the same context, since they are far apart in the document. The retriever therefore ends up finding unrelated chunks from other documents not even related to the **Menlo Group** landlord. That landlord happens to be mentioned on the first page of the file **Shorebucks LLC_NJ.pdf** file, and while one of the source chunks used by the chain is indeed from that doc that contains the correct answer (**13,500**), other source chunks from different docs are included, and the answer is therefore incorrect.


```python
chain_response["source_documents"]
```




    [Document(page_content='1.1 Landlord . DHA Group , a  Delaware  limited liability company  authorized to transact business in  New Jersey .', metadata={'xpath': '/docset:OFFICELEASE-section/docset:OFFICELEASE/docset:THISOFFICELEASE/docset:WITNESSETH-section/docset:WITNESSETH/docset:TheTerms/dg:chunk/docset:BasicLeaseInformation/docset:BASICLEASEINFORMATIONANDDEFINEDTERMS-section/docset:BASICLEASEINFORMATIONANDDEFINEDTERMS/docset:DhaGroup/docset:DhaGroup/docset:DhaGroup/docset:Landlord-section/docset:DhaGroup', 'id': 'md8rieecquyv', 'name': 'Shorebucks LLC_NJ.pdf', 'structure': 'div', 'tag': 'DhaGroup', 'Landlord': 'DHA Group', 'Tenant': 'Shorebucks LLC'}),
     Document(page_content='WITNESSES: LANDLORD: DHA Group , a  Delaware  limited liability company', metadata={'xpath': '/docset:OFFICELEASE-section/docset:OFFICELEASE/docset:THISOFFICELEASE/docset:WITNESSETH-section/docset:WITNESSETH/docset:GrossRentCreditTheRentCredit-section/docset:GrossRentCreditTheRentCredit/docset:Guaranty-section/docset:Guaranty[2]/docset:SIGNATURESONNEXTPAGE-section/docset:INWITNESSWHEREOF-section/docset:INWITNESSWHEREOF/docset:Behalf/docset:Witnesses/xhtml:table/xhtml:tbody/xhtml:tr[3]/xhtml:td[2]/docset:DhaGroup', 'id': 'md8rieecquyv', 'name': 'Shorebucks LLC_NJ.pdf', 'structure': 'p', 'tag': 'DhaGroup', 'Landlord': 'DHA Group', 'Tenant': 'Shorebucks LLC'}),
     Document(page_content="1.16 Landlord 's Notice Address . DHA  Group , Suite  1010 ,  111  Bauer Dr ,  Oakland ,  New Jersey ,  07436 , with a copy to the  Building  Management  Office  at the  Project , Attention:  On - Site  Property Manager .", metadata={'xpath': '/docset:OFFICELEASE-section/docset:OFFICELEASE/docset:THISOFFICELEASE/docset:WITNESSETH-section/docset:WITNESSETH/docset:GrossRentCreditTheRentCredit-section/docset:GrossRentCreditTheRentCredit/docset:Period/docset:ApplicableSalesTax/docset:PercentageRent/docset:PercentageRent/docset:NoticeAddress[2]/docset:LandlordsNoticeAddress-section/docset:LandlordsNoticeAddress[2]', 'id': 'md8rieecquyv', 'name': 'Shorebucks LLC_NJ.pdf', 'structure': 'div', 'tag': 'LandlordsNoticeAddress', 'Landlord': 'DHA Group', 'Tenant': 'Shorebucks LLC'}),
     Document(page_content='1.6 Rentable Area  of the Premises. 9,753  square feet . This square footage figure includes an add-on factor for  Common Areas  in the Building and has been agreed upon by the parties as final and correct and is not subject to challenge or dispute by either party.', metadata={'xpath': '/docset:OFFICELEASE-section/docset:OFFICELEASE/docset:THISOFFICELEASE/docset:WITNESSETH-section/docset:WITNESSETH/docset:TheTerms/dg:chunk/docset:BasicLeaseInformation/docset:BASICLEASEINFORMATIONANDDEFINEDTERMS-section/docset:BASICLEASEINFORMATIONANDDEFINEDTERMS/docset:PerryBlair/docset:PerryBlair/docset:Premises[2]/docset:RentableAreaofthePremises-section/docset:RentableAreaofthePremises', 'id': 'dsyfhh4vpeyf', 'name': 'Shorebucks LLC_CO.pdf', 'structure': 'div', 'tag': 'RentableAreaofthePremises', 'Landlord': 'Perry  &  Blair LLC', 'Tenant': 'Shorebucks LLC'})]



Docugami can help here. Chunks are annotated with additional metadata created using different techniques if a user has been [using Docugami](https://help.docugami.com/home/reports). More technical approaches will be added later.

Specifically, let's look at the additional metadata that is returned on the documents returned by docugami, in the form of some simple key/value pairs on all the text chunks:


```python
loader = DocugamiLoader(docset_id="wh2kned25uqm")
documents = loader.load()
documents[0].metadata
```




    {'xpath': '/docset:OFFICELEASEAGREEMENT-section/docset:OFFICELEASEAGREEMENT/docset:ThisOfficeLeaseAgreement',
     'id': 'v1bvgaozfkak',
     'name': 'TruTone Lane 2.docx',
     'structure': 'p',
     'tag': 'ThisOfficeLeaseAgreement',
     'Landlord': 'BUBBA CENTER PARTNERSHIP',
     'Tenant': 'Truetone Lane LLC'}



We can use a [self-querying retriever](../../retrievers/examples/self_query.html) to improve our query accuracy, using this additional metadata:


```python
from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever

EXCLUDE_KEYS = ["id", "xpath", "structure"]
metadata_field_info = [
    AttributeInfo(
        name=key,
        description=f"The {key} for this chunk",
        type="string",
    )
    for key in documents[0].metadata
    if key.lower() not in EXCLUDE_KEYS
]


document_content_description = "Contents of this chunk"
llm = OpenAI(temperature=0)
vectordb = Chroma.from_documents(documents=documents, embedding=embedding)
retriever = SelfQueryRetriever.from_llm(
    llm, vectordb, document_content_description, metadata_field_info, verbose=True
)
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True
)
```

    Using embedded DuckDB without persistence: data will be transient
    

Let's run the same question again. It returns the correct result since all the chunks have metadata key/value pairs on them carrying key information about the document even if this information is physically very far away from the source chunk used to generate the answer.


```python
qa_chain("What is rentable area for the property owned by DHA Group?")
```

    query='rentable area' filter=Comparison(comparator=<Comparator.EQ: 'eq'>, attribute='Landlord', value='DHA Group')
    




    {'query': 'What is rentable area for the property owned by DHA Group?',
     'result': ' 13,500 square feet.',
     'source_documents': [Document(page_content='1.1 Landlord . DHA Group , a  Delaware  limited liability company  authorized to transact business in  New Jersey .', metadata={'xpath': '/docset:OFFICELEASE-section/docset:OFFICELEASE/docset:THISOFFICELEASE/docset:WITNESSETH-section/docset:WITNESSETH/docset:TheTerms/dg:chunk/docset:BasicLeaseInformation/docset:BASICLEASEINFORMATIONANDDEFINEDTERMS-section/docset:BASICLEASEINFORMATIONANDDEFINEDTERMS/docset:DhaGroup/docset:DhaGroup/docset:DhaGroup/docset:Landlord-section/docset:DhaGroup', 'id': 'md8rieecquyv', 'name': 'Shorebucks LLC_NJ.pdf', 'structure': 'div', 'tag': 'DhaGroup', 'Landlord': 'DHA Group', 'Tenant': 'Shorebucks LLC'}),
      Document(page_content='WITNESSES: LANDLORD: DHA Group , a  Delaware  limited liability company', metadata={'xpath': '/docset:OFFICELEASE-section/docset:OFFICELEASE/docset:THISOFFICELEASE/docset:WITNESSETH-section/docset:WITNESSETH/docset:GrossRentCreditTheRentCredit-section/docset:GrossRentCreditTheRentCredit/docset:Guaranty-section/docset:Guaranty[2]/docset:SIGNATURESONNEXTPAGE-section/docset:INWITNESSWHEREOF-section/docset:INWITNESSWHEREOF/docset:Behalf/docset:Witnesses/xhtml:table/xhtml:tbody/xhtml:tr[3]/xhtml:td[2]/docset:DhaGroup', 'id': 'md8rieecquyv', 'name': 'Shorebucks LLC_NJ.pdf', 'structure': 'p', 'tag': 'DhaGroup', 'Landlord': 'DHA Group', 'Tenant': 'Shorebucks LLC'}),
      Document(page_content="1.16 Landlord 's Notice Address . DHA  Group , Suite  1010 ,  111  Bauer Dr ,  Oakland ,  New Jersey ,  07436 , with a copy to the  Building  Management  Office  at the  Project , Attention:  On - Site  Property Manager .", metadata={'xpath': '/docset:OFFICELEASE-section/docset:OFFICELEASE/docset:THISOFFICELEASE/docset:WITNESSETH-section/docset:WITNESSETH/docset:GrossRentCreditTheRentCredit-section/docset:GrossRentCreditTheRentCredit/docset:Period/docset:ApplicableSalesTax/docset:PercentageRent/docset:PercentageRent/docset:NoticeAddress[2]/docset:LandlordsNoticeAddress-section/docset:LandlordsNoticeAddress[2]', 'id': 'md8rieecquyv', 'name': 'Shorebucks LLC_NJ.pdf', 'structure': 'div', 'tag': 'LandlordsNoticeAddress', 'Landlord': 'DHA Group', 'Tenant': 'Shorebucks LLC'}),
      Document(page_content='1.6 Rentable Area  of the Premises. 13,500  square feet . This square footage figure includes an add-on factor for  Common Areas  in the Building and has been agreed upon by the parties as final and correct and is not subject to challenge or dispute by either party.', metadata={'xpath': '/docset:OFFICELEASE-section/docset:OFFICELEASE/docset:THISOFFICELEASE/docset:WITNESSETH-section/docset:WITNESSETH/docset:TheTerms/dg:chunk/docset:BasicLeaseInformation/docset:BASICLEASEINFORMATIONANDDEFINEDTERMS-section/docset:BASICLEASEINFORMATIONANDDEFINEDTERMS/docset:DhaGroup/docset:DhaGroup/docset:Premises[2]/docset:RentableAreaofthePremises-section/docset:RentableAreaofthePremises', 'id': 'md8rieecquyv', 'name': 'Shorebucks LLC_NJ.pdf', 'structure': 'div', 'tag': 'RentableAreaofthePremises', 'Landlord': 'DHA Group', 'Tenant': 'Shorebucks LLC'})]}



This time the answer is correct, since the self-querying retriever created a filter on the landlord attribute of the metadata, correctly filtering to document that specifically is about the DHA Group landlord. The resulting source chunks are all relevant to this landlord, and this improves answer accuracy even though the landlord is not directly mentioned in the specific chunk that contains the correct answer.
