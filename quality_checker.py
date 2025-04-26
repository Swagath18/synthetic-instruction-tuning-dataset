import os


class QualityChecker:
    """
    Basic rule-based quality checker for instruction-answer pairs.
    """

    def __init__(self, min_answer_words=30):
        self.min_answer_words = min_answer_words
        self.report_dir = "reports"
        os.makedirs(self.report_dir, exist_ok=True)

    def check(self, sample):
        instruction = sample.get("instruction", "").strip()
        answer = sample.get("output", "").strip()

        # Rules:
        if not instruction or not answer:
            self.log_failure(sample, "Empty instruction or answer")
            return False

        if len(answer.split()) < self.min_answer_words:
            self.log_failure(sample, f"Answer too short ({len(answer.split())} words)")
            return False

        if instruction.lower() in answer.lower():
            self.log_failure(sample, "Answer copies instruction text")
            return False

        return True

    def log_failure(self, sample, reason):
        fail_log = os.path.join(self.report_dir, "quality_failures.txt")
        with open(fail_log, "a") as f:
            f.write(f"Failure: {reason}\nInstruction: {sample['instruction']}\nAnswer: {sample['output']}\n\n")
