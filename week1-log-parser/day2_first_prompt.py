import ollama

# This is the simplest possible LLM call: one instruction, one response.
# This pattern is called "zero-shot" prompting -- you give zero examples,
# just a direct instruction, and trust the model to figure it out.

response = ollama.chat(
     model = "llama3.1",
     messages=[
         {"role": "user", "content": "Classify this log line as INFO, WARNING, or ERROR, and explain why in one sentence: '2026-06-15 03:02:11 ERROR [spark.job.daily_aggregation] OutOfMemoryError: Java heap space exceeded on executor 4'"}
    ]
    )

print(response["message"]["content"])

# Now try the SAME question 3 times and see how the wording changes
for i in range(3):
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "user", "content": "Classify this log line as INFO, WARNING, or ERROR, and explain why in one sentence: '2026-06-15 03:02:11 ERROR [spark.job.daily_aggregation] OutOfMemoryError: Java heap space exceeded on executor 4'"}
        ]
    )
    print(f"--- Attempt {i+1} ---")
    print(response["message"]["content"])
    print()
