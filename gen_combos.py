from itertools import combinations
import os

def generate_combos(header, strings, footer):
    # Ensure that the input list has at least 5 strings
    if len(strings) < 5:
        print("Error: Input list must contain at least 5 strings.")
        return

    # Generate combinations of sets of 5 strings
    combined_sets = combinations(strings, 5)
    concatenated_combinations = [''.join(comb_set) for comb_set in combined_sets]

    # Print the concatenated combinations
    i = 0
    for concatenated_combination in concatenated_combinations:
        output_file_path = os.path.join('./combos/', f'resume_{i + 1}.html')
        text_output = os.path.join('./text/', f'resume_{i + 1}.txt')

        content = f"{header}{concatenated_combination}{footer}"
        soup = BeautifulSoup(content, 'html.parser')
        raw_text = soup.get_text()

        with open(output_file_path, 'w') as output_file:
            output_file.write(content)
        with open(text_output, 'w') as output_file:
            output_file.write(raw_text)

        print(f'Combination {i + 1} written to: {output_file_path}')
        i += 1


header = '''<!DOCTYPE html>
<html>
<head>
    <title>Resume</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>

        .center-contact {
            text-align: center;
        }
        .section-break {
            border-top: 2px solid #333;
            margin: 0;
            padding: 0;
        }
        .dated_section {
            margin-top: 4px;
            margin-bottom: 4px;
        }
        .certified-link {
            text-decoration: none;
            color: #007BFF;
        }
        .contact {
          padding: 0;
          margin: 0;
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        <div class="row mt-2">
            <div class="col-md-8">
                <h1>Your Name</h1>
            </div>
            <div class="col-md-4">
                <p class="contact"><a href="mailto:your_email@gmail.com">your_email@gmail.com</a></p>
                <p class="contact"><a href="tel:+1">your_num</a></p>
            </div>
        </div>
        <div class="row">
            <div class="col-md-8">
                <h2 class="dated_section">Skills</h2>
            </div>
            <div class="col-md-4">
                <p class="contact"><a href="https://github.com/Your_git_username">github.com/Your_git_username</a></p>
                <p class="contact" style="margin-bottom: 5px"><a href="https://www.linkedin.com/in/your_linkedin/">linkedin.com/in/your_linkedin/</a></p>
            </div>
        </div>
        <div class="section-break"></div>
        <div class="row mt-4">
            <div class="col-md-8">
                <ul>
                    <li><strong>Languages:</strong> Rust, Python, Java, Javascript, C, C++</li>
                    <li><strong>Libraries:</strong> JavaFX, JDBC,jQuery, MySQL, OpenAI API, PostgreSQL, Rayon, streamlit, Serde, Tensorflow, Tokio, Yew,  </li>
                    <li><strong>Tools:</strong> GNU/Linux, Git, GitLab, REST APIs, NixOS & Docker Packaging, WASM</li>
                </ul>
            </div>
        </div>
        <h2 class="dated_section">Projects</h2>
        <div class="section-break"></div>'''
string_list = ['''<h4 id="flowgorithm-save-file-parser">Flowgorithm-Save-File-Parser - <a href="https://github.com/JustBobinAround/Flowgorithm-Save-File-Parser">Repository Link</a></h4>
<ul>
    <li>Streamlined Flowgorithm file creation from pseudo code in Python, eliminating the need for GUI and accelerating prototyping.</li>
    <li>Aided Mac and Linux users in college course to complete class without needing required windows software</li>
    <li>Shows understanding in interpreter design and dynamic programming concepts</li>
</ul>''',
'''<h4 id="adventurepuzzle">AdventurePuzzle - <a href="https://github.com/JustBobinAround/AdventurePuzzle">Repository Link</a></h4>
<ul>
    <li>Created dynamic choose-your-own-adventure website using JavaScript, hosted on GitHub Pages.</li>
    <li>Collaborated on AdventurePuzzle-Builder, a JavaFX app for story development with a user-friendly GUI.</li>
    <li>Implemented engaging storytelling with user decisions shaping the narrative, enhancing interactivity.</li>
</ul>''',
'''<h4 id="bevy-game-of-life">Bevy Game of Life - <a href="https://github.com/JustBobinAround/bevy_game_of_life">Repository Link</a> - <a href="https://justbobinaround.github.io/bevy_game_of_life/">DEMO</a></h4>
<ul>
    <li>Developed Rust project compiled to WebAssembly for Conway&#39;s Game of Life.</li>
    <li>Adapted project from logic gate simulator to Conway&#39;s Game of Life for practicality.</li>
    <li>Proficiently used Bevy game engine, showcasing Rust, Wasm, and JavaScript integration.</li>
</ul>''',
'''<h4 id="rust_pathfinding_algorithm">rust_pathfinding_algorithm - <a href="https://github.com/JustBobinAround/rust_pathfinding_algorithm">Repository Link</a></h4>
<ul>
    <li>Developed a pathfinding algorithm with dynamic obstruction generation.</li>
    <li>Implemented pathfinding for multiple points on generated maps, showcasing algorithmic and Rust skills.</li>
    <li>Designed visual display of maps with efficient algorithm processing for user interface and optimization proficiency.</li>
</ul>''',
'''<h4 id="jef-jef-explores-files">File Explorer and Fuzzy Finder - <a href="https://github.com/JustBobinAround/JEF">Repository Link</a></h4>
<ul>
    <li>Developed lightning-fast terminal file manager in Rust for power users.</li>
    <li>Enables efficient file exploration with custom hashing and Rayon multi-threading. 300K files/sec</li>
    <li>Streamlined navigation and management with a fast fuzzy finder and extensive file-opening capabilities.</li>
</ul>''',
'''<h4 id="string_enum">string_enum - <a href="https://github.com/JustBobinAround/string_enum">Repository Link</a></h4>
<ul>
    <li>Created procedural macro for auto-generating <code>str_match</code> method on enums for GPT integration.</li>
    <li>Implemented Rust solution to streamline GPT integration, enhancing readability.</li>
    <li>Shows proficiency in Rust&#39;s procedural macros, reducing enum handling boilerplate in projects.</li>
</ul>''',
'''<h4 id="-htmx_server-"><em>htmx_server - <a href="https://github.com/JustBobinAround/htmx_server">Repository Link</a></em></h4>
<ul>
    <li>Streamlined server-side htmx components in Rust.</li>
    <li>Minimalist code for shipping htmx and Rust stack apps.</li>
    <li>Early-stage development with integrated Maud&#39;s HTML! macro, basic HTTP server, router, and state management.</li>
</ul>''',
'''<h4 id="vector_node">vector_node - <a href="https://github.com/JustBobinAround/vector_node">Repository Link</a></h4>
<ul>
    <li>Implemented K-D tree structure in Rust for web page searching based on vector embeddings.</li>
    <li>Created binary traversal for faster (O(log(n)) search by sorting pages by proximity in vector space.</li>
    <li>Currently adding a REST API to interact with Vector Database</li>
</ul>''',
'''<h4 id="openai_api">openai_api - <a href="https://github.com/JustBobinAround/openai_api">Repository Link</a></h4>
<ul>
    <li>Developed Rust library for interaction with OpenAI&#39;s REST API.</li>
    <li>Specialized in language model completions and text embeddings.</li>
    <li>Integrated helper macros for efficient creation of prompts</li>
</ul>''']

footer = '''<h2 class="dated_section">Professional Experience</h2>
        <div class="section-break"></div>
        <div class="row mt-3">
            <div class="col-md-8">
                <h4>Your_job</h4>
                <ul>
                    <li>info 1</li>
                    <li>info 2</li>
                    <li>info 3</li>
                </ul>
            </div>
            <div class="col-md-4">
                <h4>1/2022 - 10/2022</h4>
            </div>
        </div>
<h2 class="dated_section">Education and Certifications</h2>
        <div class="section-break"></div>
        <div class="row mt-4">
            <div class="col-md-8">
                <h4>BS in Computer Science </h4>
                <p>info here</p>
            </div>
            <div class="col-md-4">
                <h4>10/2022 - 10/2023</h4>
            </div>
        </div>
        <div class="row">
            <div class="col-md-8">
                <h4>SOME CERT </h4>
                <p>cert desc</p>
            </div>
            <div class="col-md-4">
                <h4>01/2023</h4>
            </div>
        </div>
    </div>
</body>
</html>'''

# Example usage
generate_combos(header,string_list,footer)

