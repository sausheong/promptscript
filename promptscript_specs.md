PromptScript is a pseudolanguage designed to structure and clarify interactions with AI models like GPT-4. It allows users to express complex tasks, rules, and heuristics, helping the AI understand the tasks more accurately.

1. **Directives**: These set the context for an instruction. Begin a directive with `#`. The following directives can be used: `#story`, `#technical`, `#informal`, `#formal`. Use `#heuristic` when defining heuristics. Example: 
    ```
    #technical 
    explain {quantum physics}
    ```

2. **Action Words**: Standard English verbs that define the task for the AI. These include but are not limited to `describe`, `explain`, `list`, `summarize`. Example: `describe {the Eiffel Tower}`

3. **Objects**: The main subjects or objects of a task are enclosed in curly braces `{}`. Example: `explain {the theory of relativity}`

4. **Parameters**: Additional details or specifications are enclosed in parentheses `()`. Example: `describe {a lion} (in its natural habitat)`

5. **Flags**: Optional features or modifiers that modify a task. Flags begin with `-`. Example: `describe {a picturesque sunset} -verbose`

6. **Chaining**: Use `->` to chain multiple tasks together. The output of one task becomes the input of the next. Example: `#technical extract {key points from an article} -> summarize {the key points} -brief`

7. **Conditionals**: The `if...then...else...end` structure allows for different tasks depending on conditions. Enclose the condition in square brackets `[]`. Example: 
    ```
    #story 
    if [the character is {brave}] then 
        describe {them facing a dragon} 
    else 
        describe {them running away}
    end
    ```

8. **Variables**: Use `:=` to define a variable and `$` to refer to it later. Example: `#technical variable := {gravity} -> explain {$variable} -simple`

9.  **Loops**: The `for...do...end` structure allows for repetition of tasks. Example: 
    ```
    #technical 
    for {each planet in the solar system} do 
        describe {the planet} -brief
    end
    ```
10. **Heuristics**: Reusable sequences of tasks are defined with the `#heuristic...end` structure. Call these later by simply using their name. Example: 
    ```
    #heuristic describePlanets
    for {each planet in the solar system} do
        describe {the planet} -verbose
    end

    describePlanets
    ```

11. **Callout**: Use `python` directive to call Python statements. Enclose the Python statement in square brackets `[]`. Example: `python[print('hello world')]` will call the Python statement `print('hello world')`.