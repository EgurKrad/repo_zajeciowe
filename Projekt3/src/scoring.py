def calculate_combined_score(metrics):
    return (
        0.5 * metrics["recall"]
        + 0.3 * metrics["f1"]
        + 0.2 * metrics["accuracy"]
        - 0.1 * metrics["loss"]
    )