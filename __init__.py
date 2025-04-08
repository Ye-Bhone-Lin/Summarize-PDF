from Discord_bot.class_summarize import *

testing: ReadFile = ReadFile.load_pdf(r"D:\Programming\Summarize-PDF\src\Discord_bot\IRT_Machine_Translation.pdf")

summarize_pdf: FullSummarize = FullSummarize.full_summarize(testing)
print("Full: ", summarize_pdf)

range_summarize: UserRangeSummarize = UserRangeSummarize.range_summarize(documents=testing, start_user_page= 0, end_user_page=4)
print("Range:", range_summarize)

qa: Retriever = Retriever.retrieve(testing)
print(qa)

final: Questions_and_Answers = Questions_and_Answers.qa_chain(qa, user_question="How to evaluate")
print(final)