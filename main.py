from aptos_sdk.account import Account
from core.client import AptosClient
from utils.file import write_lines
from utils.file import read_lines
from itertools import cycle
from utils.log import log
from uuid import uuid4
from core.constants import CAMPAIGNS
import asyncio
import httpx


async def start_work(semaphore, client, session, seed_phrase):
    async with semaphore:
        private_key = client.mnemonic_to_private_key(seed_phrase)
        wallet = Account.load_key(private_key)
        result = await client.check_eligibility(session, wallet,
                                                CAMPAIGNS["Quest Four - Aptos Ecosystem Fundamentals"]
                                                ["credentials"]["On-Chain Task Verification"])
        await asyncio.sleep(2)

        if result:
            return result, private_key

        else:
            return result, seed_phrase


async def main():
    proxies = read_lines("files/proxies.txt")
    proxies_set = set()
    unique_proxies = []

    for proxy in proxies:
        if not (proxy in proxies_set):
            proxies_set.add(proxy)
            unique_proxies.append(proxy)

    if len(unique_proxies) == 0:
        log.critical("Работа без прокси невозможна")
        return

    client = AptosClient()
    semaphore = asyncio.Semaphore(len(proxies))
    timeout = httpx.Timeout(15, read=None)
    sessions = [httpx.AsyncClient(headers={"accept-language": "en,en-US;q=0.9",
                                           "content-type": "application/json",
                                           "Request-Id": str(uuid4())},
                                  proxies={"all://": proxy},
                                  timeout=timeout) for proxy in unique_proxies]
    seed_phrases = read_lines("files/seed_phrases.txt")
    seed_phrases = list(dict.fromkeys(seed_phrases))
    tasks = [asyncio.create_task(start_work(semaphore, client, session, seed_phrase)) for seed_phrase, session in
             zip(seed_phrases, cycle(sessions))]
    results = await asyncio.gather(*tasks)
    eligible_wallets = [private_key for result, private_key in results if result]
    not_eligible_wallets = [seed_phrase for result, seed_phrase in results if not result]
    write_lines("files/eligible_wallets.txt", "\n".join(eligible_wallets))
    write_lines("files/not_eligible_wallets.txt", "\n".join(not_eligible_wallets))

if __name__ == "__main__":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    except Exception:
        pass

    asyncio.run(main())
