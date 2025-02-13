import logging
import shutil
import time

from curate_gpt import ChromaDBAdapter
from curate_gpt.agents.chat_agent import ChatAgent
from curate_gpt.extract import BasicExtractor
from curate_gpt.wrappers.literature import PubmedWrapper
from tests import OUTPUT_DIR

TEMP_PUBMED_DB = OUTPUT_DIR / "pmid_tmp"

# logger = logging.getLogger(__name__)

logging.basicConfig()
logger = logging.root
logger.setLevel(logging.DEBUG)


def test_pubmed_by_id():
    extractor = BasicExtractor()
    pubmed = PubmedWrapper(extractor=extractor)
    objs = pubmed.objects_by_ids(["12754706"])
    assert len(objs) == 1


def test_pubmed_to_pmc():
    extractor = BasicExtractor()
    pubmed = PubmedWrapper(extractor=extractor)
    pmcid = pubmed.fetch_pmcid("PMID:35663206")
    assert pmcid == "PMC:PMC9159873"


def test_full_text():
    extractor = BasicExtractor()
    pubmed = PubmedWrapper(extractor=extractor)
    txt = pubmed.fetch_full_text("PMID:35663206")
    print(len(txt))
    print(txt[0:100])
    print(txt)


def test_pubmed_search():
    shutil.rmtree(TEMP_PUBMED_DB, ignore_errors=True)
    db = ChromaDBAdapter(str(TEMP_PUBMED_DB))
    extractor = BasicExtractor()
    db.reset()
    pubmed = PubmedWrapper(local_store=db, extractor=extractor)
    results = list(pubmed.search("acinar cells of the salivary gland"))
    assert len(results) > 0
    top_result = results[0][0]
    print(top_result)
    time.sleep(0.5)
    results2 = list(pubmed.search(top_result["title"]))
    assert len(results2) > 0


def test_pubmed_chat():
    shutil.rmtree(TEMP_PUBMED_DB, ignore_errors=True)
    db = ChromaDBAdapter(str(TEMP_PUBMED_DB))
    extractor = BasicExtractor()
    db.reset()
    pubmed = PubmedWrapper(local_store=db, extractor=extractor)
    chat = ChatAgent(knowledge_source=pubmed, extractor=extractor)
    response = chat.chat("what diseases are associated with acinar cells of the salivary gland")
    print(response)
