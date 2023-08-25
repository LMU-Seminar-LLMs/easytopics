from sklearn.datasets import fetch_20newsgroups
import pandas as pd
newsgroups_test = fetch_20newsgroups(subset='test')

df = pd.DataFrame({"text": newsgroups_test.data, "target": newsgroups_test.target})
df["target_names"] = df.target.apply(lambda x: newsgroups_test.target_names[x])
df = df[df.target_names.str.startswith("comp")]

# group df by target and sample 20 documents per group
df = df.groupby("target_names").apply(lambda x: x.sample(20, random_state=6482))

print(df.shape)
print(df["target_names"].value_counts())

# save to csv
df.to_csv("20newsgroup_data_comp_20perCl.csv", index=False, sep=";")
