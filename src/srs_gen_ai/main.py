
from pydantic import BaseModel
from random import randint
from crewai.flow import Flow, listen, start
from srs_gen_ai.crews.srs_crew.srs_crew import SRSCrew

class SRSState(BaseModel):
    """Maintains the state for the SRS Flow."""
    input_text: str = ""
    srs_document: str = ""


class SRSFlow(Flow[SRSState]):
    """Main flow orchestrating the SRS generation process."""

    @start()
    def generate_random_input(self):
        print("Generating random sample input")
        self.state.input_text = f"System requirement sample #{randint(1, 100)}"

    @listen(generate_random_input)
    def generate_srs(self):
        print("Generating SRS Document...")

        result = (
            SRSCrew()
            .crew()
            .kickoff(inputs={
                "requirement_text": self.state.input_text,
                "output_format": "PDF"
            })
        )


        print("✅ SRS Document Generated:\n", result.raw)
        self.state.srs_document = result.raw

    @listen(generate_srs)
    def save_srs_document(self):
        print("Saving SRS Document to file...")
        with open("srs_document.txt", "w", encoding="utf-8") as f:
            f.write(self.state.srs_document)
        print("✅ SRS Document saved to srs_document.txt")


def kickoff():
    """Run the flow normally."""
    srs_flow = SRSFlow()
    srs_flow.kickoff()


def plot():
    """Visualize the flow graph (optional)."""
    srs_flow = SRSFlow()
    srs_flow.plot()


if __name__ == "__main__":
    kickoff()
