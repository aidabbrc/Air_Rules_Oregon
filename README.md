# Air_Rules_Oregon: Oregon Air Quality Rules Query App

**RAir_Rules_Oregon** Air_Rules_Oregon is a Streamlit application that enables users to query the Oregon Administrative Rules related to air quality, managed by the Oregon Department of Environmental Quality (DEQ). Using Retrieval-Augmented Generation (RAG), this app provides context-grounded responses based on official rule documents stored in a vector database.

## Features

- Allows users to ask questions about Oregon DEQ air quality regulations.
- Retrieves relevant document chunks from a local database.
- Uses LangChain and OpenAI API to generate responses solely from retrieved documents, ensuring accuracy.
- Displays sources and text chunks to maintain transparency.

## Setup Instructions

### Prerequisites

1. Python 3.7 or higher
2. OpenAI API Key
3. Git (for version control and deployment)

### 1. Clone the Repository

```bash
git clone https://github.com/<username>/RAir_Rules_Oregon.git
cd Air_Rules_Oregon