import os
import subprocess
from pydantic import BaseModel
from random import randint
from crewai.flow import Flow, listen, start
from srs_gen_ai.crews.srs_crew.srs_crew import SRSCrew


class SRSState(BaseModel):
    """Maintains the state for the SRS Flow."""
    input_text: str = ""
    srs_document: str = ""  # This will hold the LaTeX content


class SRSFlow(Flow[SRSState]):
    """Main flow orchestrating the SRS generation process."""

    @start()
    def generate_random_input(self):
        print("Generating random sample input")
        self.state.input_text = (
            "The system is an online event booking and management platform for corporate conferences. "
            "Users should be able to register using their email or corporate single sign-on. "
            "Event organizers must be able to create events with details such as name, description, start and end dates, location, and ticket pricing. "
            "The system should allow attendees to purchase tickets securely using major credit cards and PayPal. "
            "Upon successful payment, an electronic ticket with a unique QR code should be emailed to the attendee. "
            "Attendees should also be able to download invoices from their profile. "
            "The platform must support at least 10,000 concurrent users with a response time of under 2 seconds for all main operations. "
            "The system must comply with GDPR and ensure all sensitive user data is encrypted both in transit and at rest. "
            "The platform should integrate with Zoom and Microsoft Teams for hybrid events. "
            "Administrators should have a dashboard for analytics, including ticket sales, attendee demographics, and feedback surveys. "
            "The platform should provide automated email reminders to attendees 24 hours before the event starts. "
            "Cancellations and refunds should follow customizable policies set by the event organizers. "
            "The system must be accessible via desktop and mobile browsers, with a responsive and user-friendly interface. "
            "Any feature related to hotel booking or travel planning is out of scope for this version."
        )

    @listen(generate_random_input)
    def generate_srs(self):
        print("Generating SRS LaTeX Document...")

        result = (
            SRSCrew()
            .crew()
            .kickoff(inputs={
                "requirement_text": self.state.input_text,
                "output_format": "LaTeX",
                "text": self.state.input_text, 
                
            })
        )

        self.state.srs_document = result.raw
        print("✅ SRS LaTeX Document Generated.")

    @listen(generate_srs)
    def save_and_compile_latex(self):
        tex_filename = "srs_document.tex"
        pdf_filename = "srs_document.pdf"

        print("Saving LaTeX file...")
        with open(tex_filename, "w", encoding="utf-8") as tex_file:
            tex_file.write(self.state.srs_document)
        print("✅ LaTeX file saved.")

        print("Compiling LaTeX to PDF...")
        try:
            subprocess.run(
                ["pdflatex", tex_filename],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ PDF compiled successfully to {pdf_filename}")
        except subprocess.CalledProcessError:
            print("❌ Failed to compile LaTeX to PDF. Check LaTeX syntax or pdflatex installation.")

        # Optional: clean up .aux/.log if desired
        for ext in [".aux", ".log"]:
            aux_file = tex_filename.replace(".tex", ext)
            if os.path.exists(aux_file):
                os.remove(aux_file)


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
    plot()
