from typing import Any
import click

from agent.agent import Agent

class CLI:
    def __init__(self):
        self.agent = Agent | None = None

    def run_single(self):
        pass


    
@click.command()
@click.argument("prompt", required= False)
def main(
    prompt: str | None
):
    print(prompt)
    messages=[{"role":"user", "content":prompt}]
    asyncio.run(run(messages))
    print("done")
    
main()
    