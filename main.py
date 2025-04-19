import pandas as pd
import math
import os
from agents.lawyer import DefenseLawyer, ProsecutionLawyer
from agents.judge import Judge
from agents.witness import create_witness
from agents.defendant import Defendant
from agents.plaintiff import Plaintiff
from core.trial_manager import TrialManager


def split_case_description(description, chunk_size=2000):
    words = description.split()
    num_chunks = math.ceil(len(words) / chunk_size)
    chunks = [ ' '.join(words[i*chunk_size : (i+1)*chunk_size]) for i in range(num_chunks)]
    return chunks

def main():
    file_path = "data\data.csv"
    
    if not os.path.exists(file_path):
        print("⚠️ File not found. Please check the file path.")
        return

    cases = pd.read_csv(file_path)
    total_cases = len(cases)

    print(f"\n🎯 There are {total_cases} cases available.\n")

    case_number = int(input(f"Select a case number (0 to {total_cases-1}): ").strip())

    if not (0 <= case_number < total_cases):
        print("⚠️ Invalid case number.")
        return

    case_description = cases.iloc[case_number]['text']
    print(f"\n📄 Selected Case #{case_number}: \n{case_description[:500]}...")

    case_chunks = split_case_description(case_description)
    print(f"\n⚖️ Case description is split into {len(case_chunks)} parts due to token limits.")

    proceed = input("\nDo you want to run the trial with this case? (yes/no): ").strip().lower()

    if proceed != 'yes':
        print("🚫 Trial not started.")
        return

    prosecution = ProsecutionLawyer()
    defense = DefenseLawyer()
    judge = Judge()
    defendant = Defendant()
    plaintiff = Plaintiff()

    witnesses = [create_witness(
            name="Meena Rao",
            background="Ordinary background",
            testimony="she is a winess to crime"
        )]

    trial = TrialManager(
        prosecution=prosecution,
        defense=defense,
        judge=judge,
        defendant=defendant,
        plaintiff=plaintiff,
        witnesses=witnesses
    )

    for chunk in case_chunks:
        trial.run_opening_statements(chunk)
        trial.run_witness_interrogation()
        trial.run_closing_statements()
        trial.run_judgement()

if __name__ == "__main__":
    main()
