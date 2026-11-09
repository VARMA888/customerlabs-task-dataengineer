### Day 0 & 1
- selected the `bigquery-public-data.ga4_obfuscated_sample_ecommerce` dataset to use as the main source.
- decided to rely on `user_pseudo_id` for identity resolution as a baseline assumption.
- drew the architecture flow on paper to plan out the pipeline.

### Day 2
- finalized the production runbook in the README, adding details for failure handling, testing, and how to stay within BigQuery cost limits.
- connected the `mart_attribution` table to Google Looker Studio.
- built a dashboard to visualize the first-click vs last-click attribution matrix and the time series of conversion events.

### Day 3
- updated and pushed the polished version of the final code.
- uploaded my architecture diagram and pipeline sketch pdfs to the repo.
- updated the readme file with the final finops cost notes (explaining why i used a 7-day safe sandbox limit) and run instructions.
- did the final git push to github and wrapped up the project.