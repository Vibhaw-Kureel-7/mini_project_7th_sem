import pandas as pd
import os

def create_router_dataset():
    """
    Combines question-answer CSVs from 18 chapters into one dataset,
    taking an equal number of questions from each file, then scrambling the rows.
    """

    input_folder = "QA_Datasets"
    output_file = "Router_Dataset.csv"
    num_chapters = 18

    all_data_frames = []
    print(f"Starting to process {num_chapters} files from '{input_folder}'...")

    for i in range(1, num_chapters + 1):
        file_name = f"Chapter_{i}_QA.csv"
        file_path = os.path.join(input_folder, file_name)

        try:
            df = pd.read_csv(file_path)

            if 'question' not in df.columns:
                print(f"WARNING: 'question' column not found in {file_name}. Skipping this file.")
                continue

            df['llm'] = i
            df_subset = df[['question', 'llm']]
            all_data_frames.append(df_subset)
            print(f"Processed {file_name} with {len(df_subset)} rows.")

        except FileNotFoundError:
            print(f"ERROR: File not found - {file_path}. Skipping.")
        except pd.errors.EmptyDataError:
            print(f"WARNING: Empty file - {file_path}. Skipping.")
        except Exception as e:
            print(f"An unexpected error occurred with {file_name}: {e}")

    if not all_data_frames:
        print("No data found. Exiting.")
        return

    # Determine the smallest dataset size across all chapters
    min_size = min(len(df) for df in all_data_frames)
    print(f"\nEqualizing to {min_size} questions per chapter.")

    # Take equal number of questions from each dataset
    balanced_dfs = [df.sample(n=min_size, random_state=69) for df in all_data_frames]

    # Combine all into one large DataFrame
    combined_df = pd.concat(balanced_dfs, ignore_index=True)

    # Shuffle (scramble) the combined dataset
    scrambled_df = combined_df.sample(frac=1, random_state=96).reset_index(drop=True)

    scrambled_df.to_csv(output_file, index=False)
    print(f"\n✅ Dataset saved to '{output_file}' with {len(scrambled_df)} total rows (scrambled).")

if __name__ == "__main__":
    create_router_dataset()
