import streamlit as st
import pandas as pd
from core.trial_manager import TrialManager
from agents.lawyer import DefenseLawyer, ProsecutionLawyer
from agents.judge import Judge
from agents.defendant import Defendant
from agents.witness import create_witness

@st.cache
def load_cases():
    df = pd.read_csv("cases.csv")
    return df

def main():
    cases = load_cases()

    st.sidebar.title("Select a Case")
    case_num = st.sidebar.slider("Choose Case Number", 0, 500, 0)

    case_description = cases.iloc[case_num]['text']

    def chunk_case_description(description, max_length=3000):
        """Splits case description into manageable chunks for the model."""
        words = description.split()
        chunks = []
        current_chunk = []

        for word in words:
            current_chunk.append(word)
            if len(' '.join(current_chunk)) > max_length:
                chunks.append(' '.join(current_chunk[:-1]))
                current_chunk = [word]

        if current_chunk:
            chunks.append(' '.join(current_chunk))
        return chunks

    st.header(f"Case {case_num + 1} Description")
    st.write(case_description[:1500] + "...\n(Showing first part for brevity)")

    st.text_area("Full Case Description", case_description, height=300)

    run_trial = st.button("Run Trial")

    if run_trial:
        defense = DefenseLawyer()
        prosecution = ProsecutionLawyer()
        judge = Judge()
        defendant = Defendant()

        witnesses = [
            create_witness(
                name="Meena Rao",
                background="Forensic accountant who audited the trust.",
                testimony="The financial records had clear signs of document tampering and mismatched entries."
            ),
            create_witness(
                name="Anonymous Tipster",
                background="Former employee who leaked internal emails.",
                testimony="Emails suggested deliberate inflation of expenses and unauthorized fund transfers by Rajiv."
            )
        ]

        trial = TrialManager(
            prosecution=prosecution,
            defense=defense,
            judge=judge,
            defendant=defendant,
            witnesses=witnesses
        )

        for chunk in chunk_case_description(case_description):
            trial.run_opening_statements(chunk)
            trial.run_witness_interrogation()
            trial.run_closing_statements()
            trial.run_judgement()

if __name__ == "__main__":
    main()
