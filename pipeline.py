# from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
# from typing import Callable, Optional
# import time


# def run_pipeline(topic: str, on_progress: Optional[Callable[[str, str, dict], None]] = None) -> dict:
#     """
#     Runs the full multi-agent research pipeline.

#     on_progress(stage_key, status, payload) is called at each step so a UI
#     (like Streamlit) can render live updates. status is one of:
#     "start", "done".
#     stage_key is one of: "search", "read", "write", "critique".
#     payload is a dict that may contain "content" once a stage is done.
#     """

#     def emit(stage_key: str, status: str, **payload):
#         if on_progress:
#             on_progress(stage_key, status, payload)

#     state = {}

#     # 1. Search agent
#     print("\n " + "=" * 50)
#     print("running search agent working...")
#     print("\n " + "=" * 50)
#     emit("search", "start")

#     search_agent = build_search_agent()
#     search_result = search_agent.invoke({
#         "messages": [("user", f"find me recent, reliable and detailed information on the topic: {topic}")],
#     })
#     state["search_results"] = search_result['messages'][-1].content

#     print("\n search results: \n")
#     print(state["search_results"])
#     emit("search", "done", content=state["search_results"])

#     time.sleep(2)  # avoid Mistral free-tier rate limit (1 request/sec)

#     # 2. Reader agent
#     print("\n " + "=" * 50)
#     print("running reader agent working...")
#     print("\n " + "=" * 50)
#     emit("read", "start")

#     reader_agent = build_reader_agent()
#     reader_result = reader_agent.invoke({
#         "messages": [("user",
#                       f"Based on the following search result about '{topic}',"
#                       f"pick the most relevant URL and scrape it for deeper content .\n\n"
#                       f"Search Result:\n{state['search_results'][:800]}"
#                       )]
#     })
#     state["scraped_content"] = reader_result['messages'][-1].content

#     print("\n scraped content: \n")
#     print(state["scraped_content"])
#     emit("read", "done", content=state["scraped_content"])

#     time.sleep(2)  # avoid Mistral free-tier rate limit (1 request/sec)

#     # 3. Writer chain
#     print("\n " + "=" * 50)
#     print("writer chain working...")
#     print("\n " + "=" * 50)
#     emit("write", "start")

#     research_combined = (
#         f" SEARCH RESULTS:\n{state['search_results']}\n\n"
#         f" DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
#     )

#     state["report"] = writer_chain.invoke({
#         "topic": topic,
#         "research": research_combined
#     })

#     print("\n FINAL REPORT:\n")
#     print(state["report"])
#     emit("write", "done", content=state["report"])

#     time.sleep(2)  # avoid Mistral free-tier rate limit (1 request/sec)

#     # 4. Critic chain
#     print("\n " + "=" * 50)
#     print("critic chain working...")
#     print("\n " + "=" * 50)
#     emit("critique", "start")

#     state["feedback"] = critic_chain.invoke({
#         "report": state['report']
#     })

#     print("\n CRITIC REPORT:\n")
#     print(state["feedback"])
#     emit("critique", "done", content=state["feedback"])

#     return state


# if __name__ == "__main__":
#     topic = input("\n Enter a research topic :")
#     run_pipeline(topic)

from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
from typing import Callable, Optional
import time


def invoke_with_backoff(fn, *args, max_attempts: int = 4, base_delay: int = 10, **kwargs):
    """
    Calls fn(*args, **kwargs). If it fails with a rate-limit (429) error,
    waits base_delay, 2x, 3x... seconds and retries, up to max_attempts.
    Any other kind of error is raised immediately without retrying.
    """
    last_error = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            msg = str(e)
            is_rate_limit = "429" in msg or "rate_limited" in msg or "rate limit" in msg.lower()
            last_error = e
            if not is_rate_limit or attempt == max_attempts:
                raise
            wait_time = base_delay * attempt
            print(f"\n[rate limit] attempt {attempt}/{max_attempts} failed, "
                  f"waiting {wait_time}s before retrying...\n")
            time.sleep(wait_time)
    raise last_error


def run_pipeline(topic: str, on_progress: Optional[Callable[[str, str, dict], None]] = None) -> dict:
    """
    Runs the full multi-agent research pipeline.

    on_progress(stage_key, status, payload) is called at each step so a UI
    (like Streamlit) can render live updates. status is one of:
    "start", "done".
    stage_key is one of: "search", "read", "write", "critique".
    payload is a dict that may contain "content" once a stage is done.
    """

    def emit(stage_key: str, status: str, **payload):
        if on_progress:
            on_progress(stage_key, status, payload)

    state = {}

    # 1. Search agent
    print("\n " + "=" * 50)
    print("running search agent working...")
    print("\n " + "=" * 50)
    emit("search", "start")

    search_agent = build_search_agent()
    search_result = invoke_with_backoff(
        search_agent.invoke,
        {"messages": [("user", f"find me recent, reliable and detailed information on the topic: {topic}")]},
    )
    state["search_results"] = search_result['messages'][-1].content

    print("\n search results: \n")
    print(state["search_results"])
    emit("search", "done", content=state["search_results"])

    time.sleep(3)

    # 2. Reader agent
    print("\n " + "=" * 50)
    print("running reader agent working...")
    print("\n " + "=" * 50)
    emit("read", "start")

    reader_agent = build_reader_agent()
    reader_result = invoke_with_backoff(
        reader_agent.invoke,
        {"messages": [("user",
                      f"Based on the following search result about '{topic}',"
                      f"pick the most relevant URL and scrape it for deeper content .\n\n"
                      f"Search Result:\n{state['search_results'][:800]}"
                      )]},
    )
    state["scraped_content"] = reader_result['messages'][-1].content

    print("\n scraped content: \n")
    print(state["scraped_content"])
    emit("read", "done", content=state["scraped_content"])

    time.sleep(3)

    # 3. Writer chain
    print("\n " + "=" * 50)
    print("writer chain working...")
    print("\n " + "=" * 50)
    emit("write", "start")

    research_combined = (
        f" SEARCH RESULTS:\n{state['search_results']}\n\n"
        f" DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = invoke_with_backoff(
        writer_chain.invoke,
        {"topic": topic, "research": research_combined},
    )

    print("\n FINAL REPORT:\n")
    print(state["report"])
    emit("write", "done", content=state["report"])

    time.sleep(3)

    # 4. Critic chain
    print("\n " + "=" * 50)
    print("critic chain working...")
    print("\n " + "=" * 50)
    emit("critique", "start")

    state["feedback"] = invoke_with_backoff(
        critic_chain.invoke,
        {"report": state['report']},
    )

    print("\n CRITIC REPORT:\n")
    print(state["feedback"])
    emit("critique", "done", content=state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic :")
    run_pipeline(topic)