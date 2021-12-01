import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import scraper


def charts_setup():
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


def get_cohorts_by_size(students):

    # organize students by cohorts
    cohorts = [x[2] for x in students]

    # get the number of students in each cohort
    cohorts_with_sizes = [[cohorts.count(cohort), cohort] for cohort in set(cohorts)]

    # sort by year of graduation, and size within that
    cohorts_with_sizes_by_graduating_year = sorted(
        cohorts_with_sizes, key=lambda x: x[0], reverse=True
    )

    return cohorts_with_sizes_by_graduating_year


def plot_size_over_years(dataset):
    # get number of students per cohort organized by size
    cohorts_with_sizes_by_sizes = get_cohorts_by_size(dataset)

    # sort by graduating year
    cohorts_with_sizes_by_graduating_year = sorted(
        cohorts_with_sizes_by_sizes, key=lambda x: x[1][-2:], reverse=False
    )

    # plot bar chart
    data = pd.DataFrame(
        cohorts_with_sizes_by_graduating_year, columns=["size", "cohort"]
    )
    size_over_years_plot = sns.barplot(data=data, x="cohort", y="size")
    plt.setp(size_over_years_plot.get_xticklabels(), rotation=75)
    plt.tick_params(axis="x", labelsize=8)
    plt.tick_params(axis="y", labelsize=12)
    plt.show()


def plot_composition(dataset):

    # get number of students per cohort organized by size
    cohorts_with_sizes_by_size = get_cohorts_by_size(dataset)

    # reconfigure as two lists for donut chart
    data = list(zip(*cohorts_with_sizes_by_size))

    # configs for donut chart
    data, labels = (
        data[0],
        data[1],
    )

    # plot chart
    patches, texts, autotexts = plt.pie(
        data, labels=labels, colors=sns.color_palette("pastel"), autopct="%.0f%%"
    )

    # configs for donut chart
    [text.set_color("white") for text in texts]
    [autotext.set_color("black") for autotext in autotexts]

    # circle for donut chart
    centre_circle = plt.Circle((0, 0), 0.70, fc="black")
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.show()


def clean_data(dataset):

    # removes entries for temporary students
    # also removes identifying information for all students
    clean_dataset = [
        [
            row[0][:-7].strip() if "PHD" not in row[0] else row[0],  # program
            row[0][-7:].strip() if "PHD" not in row[0] else "",  # batch
            row[0],  # cohort
            row[4],  # status
            row[5],  # subjects pursuing
        ]
        for row in dataset
        if "VISP" not in row[0] and "YSP" not in row[0] and "VSP" not in row[0]
    ]

    return clean_dataset


def main():
    charts_setup()

    dataset = scraper.main()
    clean_dataset = clean_data(dataset)

    # get only students currently enrolled
    current_dataset = list(filter(lambda x: "Enrolled" in x[3], clean_dataset))

    '''plot_size_over_years(clean_dataset)
    plot_composition(clean_dataset)
    plot_size_over_years(current_dataset)
    plot_composition(current_dataset)'''


if __name__ == "__main__":
    main()
