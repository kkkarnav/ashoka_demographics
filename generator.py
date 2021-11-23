import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pprint

import scraper


def setup():
    sns.set(rc={"figure.figsize": (11.7, 8.27)})
    sns.set(
        rc={
            "axes.facecolor": "black",
            "figure.facecolor": "black",
            "axes.edgecolor": "black",
            "axes.labelcolor": "cornflowerblue",
            "grid.color": "black",
            "xtick.color": "white",
            "ytick.color": "white",
        }
    )


def plot_size_over_years(cohort_counts):

    # get each cohort sorted by year
    cohort_counts_sorted_by_year = sorted(
        sorted(cohort_counts, key=lambda x: x[1].split(" ")[0], reverse=True),
        key=lambda x: x[1].split("-")[-1],  # sorts cohorts by graduating year
        reverse=False,  # in ascending order
    )

    # plot bar chart
    data = pd.DataFrame(cohort_counts_sorted_by_year, columns=["size", "cohort"])
    size_over_years_plot = sns.barplot(data=data, x="cohort", y="size")
    plt.setp(size_over_years_plot.get_xticklabels(), rotation=75)
    plt.tick_params(axis="x", labelsize=8)
    plt.tick_params(axis="y", labelsize=12)
    plt.show()


def plot_current_composition(cohort_counts, df):

    df = df[df.status.isin(['Enrolled'])]
    df.sort_values(by=['batch'])
    pprint.pprint(df)

    # get all cohorts currently at the university, in order of enrollment
    current_cohorts = sorted(
        sorted(
            filter(
                lambda x: "2021" in x[1] or "-22" in x[1] or "-23" in x[1],
                cohort_counts,
            ),
            # only keep students currently at the university
            key=lambda x: x[0],
            reverse=False,  # in ascending order
        ),
        key=lambda x: x[1].split("-")[0].split(" ")[-1],  # sorts cohorts by intake year
        reverse=False,  # in ascending order
    )

    # configs for pie chart
    current_cohorts = sorted(current_cohorts, key=lambda x: x[0], reverse=True)
    data, labels = list(zip(*current_cohorts))[0], list(zip(*current_cohorts))[1]
    colors = sns.color_palette("pastel")[0 : len(data)]

    # plot pie chart
    patches, texts, autotexts = plt.pie(
        data, labels=labels, colors=colors, autopct="%.0f%%"
    )
    [text.set_color("white") for text in texts]
    [autotext.set_color("black") for autotext in autotexts]

    # circle for donut
    centre_circle = plt.Circle((0, 0), 0.70, fc="black")
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.show()


# get the number of cohorts and the number of students per cohort
def plot_sizes(dataset, df):

    batches = [student[0] for student in dataset]  # extract every student's cohort

    cohort_counts = list(
        filter(
            lambda x: "VISP" not in x[1] and "YSP" not in x[1] and "VSP" not in x[1],
            # remove visiting students and highschoolers
            [[batches.count(batch), batch] for batch in set(batches)],
            # compose tuple of cohort and number of students in it
        )
    )

    plot_current_composition(cohort_counts, df)
    plot_size_over_years(cohort_counts)


def plot_majors(dataset):
    subjects = (
        "ENG",
        "CS",
        "MAT",
        "PSY",
        "POL",
        "BIO",
        "PHY",
        "SOC",
        "HIS",
        "IR",
        "VA",
        "ECO",
        "CW",
        "PHI",
        "MS",
        "PPE",
        "SOA",
        "ENT",
        "ES",
        "CHM",
        "SAN",
        "FIN",
    )

    subjects_by_cohort = {}
    for cohort_year in range(17, 24):
        cohort = [
            x[-1]
            for x in filter(
                lambda x: "UG" in x[0] and "-" + str(cohort_year) in x[0], dataset
            )
        ]
        cohort_subjects = [
            len(list(filter(lambda x: subject in x, cohort))) for subject in subjects
        ]
        subjects_by_cohort[cohort_year] = cohort_subjects

    for cohort in subjects_by_cohort.values():
        print(cohort[0])


def clean_data(dataset):

    # removes temporary students
    clean_dataset = [
        row
        for row in dataset
        if "VISP" not in row[0] and "YSP" not in row[0] and "VSP" not in row[0]
    ]

    for row in clean_dataset:
        if "Pragya" in row[3]:
            print(row)

    df = pd.DataFrame(
        clean_dataset, columns=["batch", "email", "id", "name", "status", "subjects"]
    )
    df.drop(["email", "id", "name"], axis=1)

    return df


def main():
    setup()

    dataset = scraper.main()
    df = clean_data(dataset)
    plot_sizes(dataset, df)
    plot_majors(dataset)


if __name__ == "__main__":
    main()
