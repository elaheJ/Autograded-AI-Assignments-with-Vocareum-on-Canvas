# Sources and attribution

## Platform workflow

The guides synthesize the repository owner's notebook-authoring and deployment workflow with the following primary references, reviewed October 14, 2026:

- [Vocareum notebook grading and publishing](https://help.vocareum.com/en/articles/9341352-setting-up-grading-in-vocareum-notebook)
- [Vocareum folders and learner update behavior](https://help.vocareum.com/en/articles/9341349-navigating-the-vocareum-files-browser)
- [Vocareum Canvas LTI setup and grade mapping](https://help.vocareum.com/en/articles/5085436-lti-1-3-setup-guide-for-canvas)
- [nbgrader assignment creation and grading](https://nbgrader.readthedocs.io/en/stable/user_guide/creating_and_grading_assignments.html)

These links describe the underlying platforms; they do not imply endorsement or institution-wide compatibility. Menu labels and permissions may vary.

## Arena Tools

The optional live activity reads the [Arena aggregate leaderboard dataset](https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset), attributed to **lmarena-ai**. The source identifies its data license as **CC BY 4.0**. Consult the current dataset card and its license before redistributing retrieved results. This repository contains software test fixtures, not a leaderboard dataset snapshot.

The optional controller uses a Chat Completions-compatible tool-calling interface; consult the provider's documentation and terms. The teaching notebook links to [OpenAI function-calling documentation](https://developers.openai.com/api/docs/guides/function-calling).

## QLoRA demo

The demo was adapted from the repository owner's QLoRA teaching activity into four independently scored code blocks. It uses a Python model stand-in and does not distribute a pretrained model, external book chapter, or a full fine-tuning implementation.

For the method's research background, see [QLoRA Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314), Dettmers and colleagues, 2023. The toy model's parameter counts are not measurements of a real language model.

## License scope

The [MIT license](LICENSE) covers this repository's guidelines and example code. Linked documentation, retrieved data, third-party packages, and external models remain governed by their respective terms.
