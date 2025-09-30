import os
from typing import List, Dict
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process,LLM,Process
from dotenv import load_dotenv
load_dotenv()

from scrapingdog_tool import scrapingdog_tool


llm= LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    #provider="google",
    temperature=0.7, # high temperature means more creative responses
    timeout=120 # api call kr k 120 sec wait kro (good for long responses and slow internet connections)
)

hf_llm = LLM(
    model="huggingface/meta-llama/Llama-3.1-8B-Instruct",  
    provider="huggingface"

)

tools = [scrapingdog_tool()]


blog_scraper = Agent(
    name="Blog Scraper",
    role="Web Content Researcher",
    backstory="You are an expert web content researcher. Your task is to extract complete and accurate information from websites.",
    goal="Extract complete and accurate information from a blog URLs",
    verbose=True,
    allow_delegation=False,
    llm=hf_llm,
    tools=tools
)

blog_summarizer = Agent(
    name="Blog Summarizer",
    role="Content Analyst",
    goal="Create concise and informative summaries of blog content",
    backstory="You are an expert content analyst. Your task is to create concise, informative summaries of the blog content provided to you by the user. You will use the LLM to generate summaries based on the content extracted by the Blog Scraper agent.",
    llm=hf_llm,
    verbose=True,
    allow_delegation=False)

#here we used function and not like documentation coz we need to pass url
def scrape_blog_task(url):
    return Task(
        # this is how you make it multi line
        description= (f"Scrape the contentfrom the blog at {url} using ScrapingDog API."
                      "Extract the main content,including text and any other relevant information, filtering out ads, and other non-essential elements."
                      ),
        expected_output="Full text content of the blog in markdown format.",
        agent=blog_scraper
    )

def summarize_blog_task(scrape_task):
    # task ka object h yeh task class ka
    return Task(
        description=("Summarize the blog content provided by the Blog Scraper agent. "
        "Create a concise and informative summary that captures the main points and key insights from the blog."),

        expected_output=("A well-structured concise summary of the blog post in 100-200 words."
                         "The summary will be used to generate a podcast script."
                         "Summary should be suitable suitable for a podcast script."
                         ),
        agent=blog_summarizer,
        context=[scrape_task]
    )

def create_blog_summary_crew(url):
    scrape_task =scrape_blog_task(url)
    summarize_task = summarize_blog_task(scrape_task)

    crew = Crew(
        agents= [blog_scraper, blog_summarizer],
        tasks= [scrape_task, summarize_task],
        verbose=True,
        process=Process.sequential
    )
    return crew


#ismy summary h hamari jo hum frontend ko dey raha hein
def summarize_blog(url):
    crew = create_blog_summary_crew(url)
    result = crew.kickoff()
    return result.raw


if __name__ == "__main__":
    url = "https://digitaloneagency.com.au/smart-contract-builder-for-wills-and-trusts-the-future-of-digital-asset-inheritance/"
    summary = summarize_blog(url)
    print("\n[ 📝 Blog Summary ]\n")
    print(summary)