from src.orchestration.IndexingOrchestrator import IndexingOrchestrator


def main():

    orchestrator = IndexingOrchestrator(
        config_path="config/config.yaml"
    )

    orchestrator.run(
        input_path="data/raw"
    )


if __name__ == "__main__":
    main()