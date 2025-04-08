import discord
from function_tools import ReadFile, FullSummarize, UserRangeSummarize, Retriever, Questions_and_Answers
from groq import APIStatusError
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        try:
            pdf_attachments = [a for a in message.attachments if a.filename.lower().endswith('.pdf')]
            if len(pdf_attachments) >= 1:
                combined_docs = []

                for attachment in pdf_attachments:
                    await attachment.save(attachment.filename)
                    print(f"Saved PDF: {attachment.filename}")
                    docs = ReadFile.load_pdf(attachment.filename)
                    combined_docs.extend(docs)  
                    os.remove(attachment.filename)
                    
                await message.channel.send(
                        """📚 **PDF Bot Functions**

                    1️⃣ **Summarize PDF**  
                    ‣ Get a short and clear summary of your document.

                    2️⃣ **Q&A Mode**  
                    ‣ Ask questions about the PDF and get instant answers.
            
                    """
                    )
                user_choice = await self.wait_for("message", check=lambda m: m.author == message.author)
                choice = user_choice.content.strip().lower()

                if choice == "summarize":
                    await message.channel.send("Would you like to summarize all pages or specify a range? Type 'all' for all or 'range' for a specific range.")
                    response = await client.wait_for('message', check=lambda m: m.author == message.author)

                    if response.content.lower() == "all":
                        summarize_pdf = FullSummarize.full_summarize(combined_docs)
                        await message.channel.send(summarize_pdf)
                    
                    elif response.content.lower() == "range":
                        await message.channel.send("Please specify the page range (e.g., '3-7').")
                        page_range = await client.wait_for('message', check=lambda m: m.author == message.author)
                        
                        try:
                            start, end = map(int, page_range.content.split('-'))
                            user_range_summarize_pdf = UserRangeSummarize.range_summarize(documents=combined_docs, start_user_page=start, end_user_page=end)
                            await message.channel.send(user_range_summarize_pdf)
                        
                        except ValueError:
                            await message.channel.send("Sorry, I couldn't understand the page range. Please use the format 'start-end'.")                        
                
                elif choice in ["q&a", "qa", "questions and answers"]:
                    await message.channel.send("💬 Please type your question about the PDF:")

                    while True:
                        try:
                            question_msg = await client.wait_for(
                                "message",
                                check=lambda m: m.author == message.author and m.channel == message.channel
                            )

                            if question_msg.content.lower() in ["exit", "done", "quit"]:
                                await message.channel.send("👋 Exiting Q&A mode.")
                                break

                            qa: Retriever = Retriever.retrieve(combined_docs)
                            final: Questions_and_Answers = Questions_and_Answers.qa_chain(qa, user_question=question_msg.content)

                            try:
                                await message.channel.send(final)
                            
                            except discord.HTTPException as e:
                                if "Must be 2000 or fewer in length" in str(e):
                                    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False, suffix=".txt") as tmp:
                                        tmp.write(final)
                                        tmp_path = tmp.name

                                    await message.channel.send(
                                        "⚠️ Discord limit error, so here's an answer file:",
                                        file=discord.File(tmp_path)
                                    )

                                    os.remove(tmp_path)
                                else:
                                    raise

                        except Exception as e:
                            await message.channel.send(f"⚠️ An error occurred: `{e}`")       
                else:
                    await message.channel.send("Write again!. You have to choose 'Summarize' or 'Questions and Answers")                        
        
        except APIStatusError as e:
            if e.status_code == 413:
                await message.channel.send("Server is busy. Try with only one pdf.")
            else:
                # Handle other APIStatusErrors
                await message.channel.send("Server is busy.")
            
intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(os.getenv('DISCORD_KEY'))
