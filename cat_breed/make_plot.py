import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_data():
    return pd.read_csv("data.csv")

def perform_pca(X):
    pca = PCA(n_components=2)
    pca.fit(X)
    print(pca.explained_variance_ratio_)
    print(pca.singular_values_)
    print (pca.components_)
    return pca.transform(X)

def find_best_num_clusters(X):
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, n_init='auto', random_state=0)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), wcss, marker='o', linestyle='--', color='b')
    plt.title('Elbow Method for Optimal k')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('WCSS (Within-Cluster Sum of Squares)')
    plt.grid(True)
    plt.savefig("kmean_wcss.jpg")

def main():
    df = get_data()

    # add pca
    X = df[['Affection', 'Playfulness', 'Energy', 'Vocalness', 'Intelligence']].values
    Y = perform_pca(X)
    df_pca = pd.DataFrame(Y, columns=["pc1", "pc2"])
    for col in df_pca.columns:
        df_pca[col] += np.random.uniform(-0.1, 0.1, size=len(df_pca))
    df = pd.concat([df, df_pca], axis=1)

    # kmean clustering
    find_best_num_clusters(X)
    best_num_clusters = 4 # by looking at the output plot from find_best_num_clusters
    kmeans = KMeans(n_clusters=best_num_clusters, random_state=0, n_init="auto").fit(X)
    df['cluster'] = kmeans.labels_
    for cluster, tt in df.groupby('cluster'):
        print ("cluster", cluster, "include these breads: ", list(tt['Breed'].values))

    # make clustering plot
    fig = px.scatter(
        df,
        x="pc1",
        y="pc2",
        text="Breed",
        hover_data={
            "Breed": True,
            "Affection": True,
            "Playfulness": True,
            "Energy": True,
            "Vocalness": True,
            "Intelligence": True,
            "pc1": False,
            "pc2": False,
            "cluster": False
        },
        title="Cat Breeds",
        color="cluster",
        labels={"pc1": "Overal energy (Low -> High)", 'pc2': "Overall affectionate (Low -> High)"}
    )

    fig.update_traces(textfont=dict(color='rgba(0,0,0,0.3)', size=10), marker=dict(size=12), textposition='top center')

    # Custom hovertemplate with bold breed name
    fig.update_traces(
        hovertemplate=(
            '<b>%{customdata[0]}</b><br>' +
            'Affection: %{customdata[1]}<br>' +
            'Playfulness: %{customdata[2]}<br>' +
            'Energy: %{customdata[3]}<br>' +
            'Vocalness: %{customdata[4]}<br>' +
            'Intelligence: %{customdata[5]}<extra></extra>'
        ),
        customdata=df[['Breed', 'Affection', 'Playfulness', 'Energy', 'Vocalness', 'Intelligence']].values
    )

    # Customize hover label font and make mobile responsive
    fig.update_layout(
        hoverlabel=dict(
            font_size=14,
            font_family="Arial",
            bgcolor="white",
            font_color="black"
        ),
        hovermode='closest',
        height=None,  # Remove fixed height to allow responsive behavior
        autosize=True,
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(size=12),
        title_font=dict(size=16),
        xaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=10)
        ),
        legend=dict(
            font=dict(size=11),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )


    # Save as HTML file with responsive configuration
    fig.write_html("cat_breeds_interactive_plot.html", 
                   config={'responsive': True, 'displayModeBar': True})
    print("Interactive plot saved as 'cat_breeds_interactive_plot.html'")

if __name__=="__main__":
    main()