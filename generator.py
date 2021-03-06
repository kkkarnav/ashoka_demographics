import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pprint

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
        "CS",
        "POL",
        "ECO",
        "PHY",
        "SOC",
        "HIS",
        "VA",
        "CHM",
        "CW",
        "MAT",
        "PHI",
        "MS",
        "BIO",
        "PPE",
        "IR",
        "FIN",
        "SOA",
        "ENT",
        "ES",
        "PSY",
        "SAN",
        "ENG",
    )

    # only take UG and ASP students
    undergraduates = list(filter(lambda x: x[0] == "UG" or x[0] == "ASP", dataset))

    # subject: students studying the subject, students majoring in it, minoring in it, concentrating in it
    subjects_with_sizes = {subject: [0, 0, 0, 0] for subject in subjects}

    # iterate over every undergraduate for every subject offered
    for subject in subjects:
        for student in undergraduates:

            if subject in student[4]:
                subjects_with_sizes[subject][0] += 1
            if "Major - " + subject in student[4]:
                subjects_with_sizes[subject][1] += 1
            if "Minor - " + subject in student[4]:
                subjects_with_sizes[subject][2] += 1
            if "Concentration - " + subject in student[4]:
                subjects_with_sizes[subject][3] += 1

    # sort by number of students taking subject
    subjects_with_sizes_by_size = sorted(
        subjects_with_sizes.items(), key=lambda item: item[1][1], reverse=True
    )

    # configs for bar chart
    plot_data = [[x[1][1], x[0]] for x in subjects_with_sizes_by_size]
    pprint.pprint(plot_data)

    # plot bar chart
    data = pd.DataFrame(plot_data, columns=["size", "subject"])

    """# plot bar chart
    size_over_subjects_plot = sns.barplot(data=data, x="subject", y="size")
    plt.tick_params(axis="x", labelsize=12)
    plt.tick_params(axis="y", labelsize=12)
    plt.show()"""

    # reconfigure as two lists for donut chart
    data = list(zip(*plot_data))

    # configs for donut chart
    data, labels = (
        data[0],
        data[1],
    )

    # plot chart
    patches, texts = plt.pie(
        data,
        labels=labels,
        colors=[
            sns.color_palette("Spectral", len(labels))[subjects.index(key)]
            for key in labels
        ],
    )

    # configs for donut chart
    [text.set_color("white") for text in texts]

    # circle for donut chart
    centre_circle = plt.Circle((0, 0), 0.70, fc="black")
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.show()


def get_cohorts_by_size(students):

    # organize students by cohorts by getting the third column (program + batch) of each row
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
    print(data)
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
        data, labels=labels, colors=sns.color_palette("Spectral"), autopct="%.0f%%"
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

    plot_size_over_years(clean_dataset)
    plot_size_over_years(current_dataset)
    plot_composition(clean_dataset)
    plot_composition(current_dataset)
    plot_majors(current_dataset)
    plot_majors(row for row in clean_dataset if row not in current_dataset)


if __name__ == "__main__":
    main()
