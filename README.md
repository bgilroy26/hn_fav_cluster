# hn_fav_cluster
---
HN Favorite Data Pipeline
----
```mermaid
    flowchart LR;
        hn_scrape2 --> fav_scrapr --> get_hn_api_data --> sentence_etl --> generate_vectors;
        subgraph "get my favorites"
        hn_scrape2     
        end
        subgraph "get text from each"
        fav_scrapr
        end
        subgraph "pull comment text from HN api"
        get_hn_api_data
        end
        subgraph "load text into sqlite"
        sentence_etl
        end
        subgraph "run BERT over text"
        generate_vectors
        end

