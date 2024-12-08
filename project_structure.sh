email-webhook-app/
├── app/
│   ├── main.py                             # FastAPI entry point
│   ├── ai_agent.py                         # AI_gent ochestration script
│   ├── services/
│   │   ├── email_service.py                # Email fetching logic
│   │   ├── classify_service.py             # Classification using intent_classification.py
│   ├── reasoning_engine/
│   │   ├── reasoning_engine.py             # reasoning engine main
│   │   ├── reasoning_utils.py          
│   ├── prompts/
│   │   ├── reasoning_engine_template.md    
│   │   ├── intend-classification_guide.me 
│   │   ├── intend-classification_head.me
├── .env                                    # Environment variables
├── requirements.txt                        # Python dependencies
└── Dockerfile                              # Docker configuration
