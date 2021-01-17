import pandas as pd
import df_manipulation


def productivity_country_per_topic(df_affiliations, df_topics, normalization='both'):
    # precomputation:
    num_affs_series = df_affiliations.reset_index().groupby('article').size()  # ['affiliation']
    df_affs_topics = pd.DataFrame({'article': num_affs_series.index, 'num affs': num_affs_series.values}).set_index(
        'article').merge(df_topics, on='article').merge(df_affiliations['year'], on='article')

    df_articles_topics_distributed = df_affs_topics[df_affs_topics.columns.difference(['num affs', 'year'])].div(
        df_affs_topics.iloc[:, 0], axis='rows')
    df_articles_topics_distributed_single = df_articles_topics_distributed.reset_index().groupby('article').mean()
    df_affs_topics_distributed = df_affiliations.reset_index().set_index('article').merge(
        df_articles_topics_distributed_single, on='article')
    df_country_topics_absolute_productivity = df_affs_topics_distributed.groupby(['iso_a3', 'year']).sum()
    if normalization == 'None':
        df_country_topics_relative_productivity = df_country_topics_absolute_productivity.groupby('year').sum()
        df_country_topics_relative_productivity['normalization'] = normalization
        return df_country_topics_relative_productivity
    elif normalization == 'absolute_year':
        df_year_topics_absolute_productivity = df_country_topics_absolute_productivity.groupby('year').sum()
        df_country_topics_relative_productivity = df_year_topics_absolute_productivity.div(
            df_year_topics_absolute_productivity.sum(axis='columns'),
            axis='rows')
        df_country_topics_relative_productivity['normalization'] = normalization
        return df_country_topics_relative_productivity
    elif normalization == 'country_indipendent':
        df_productivity_None = df_country_topics_absolute_productivity.groupby('year').sum()
        df_productivity_None['normalization'] = 'None'
        df_year_topics_absolute_productivity = df_country_topics_absolute_productivity.groupby('year').sum()
        df_productivity_year = df_year_topics_absolute_productivity.div(
            df_year_topics_absolute_productivity.sum(axis='columns'),
            axis='rows')
        df_productivity_year['normalization'] = 'absolute_year'
        return pd.concat([df_productivity_None, df_productivity_year])
    elif normalization == 'local':
        df_country_topics_relative_productivity = df_country_topics_absolute_productivity.div(
            df_country_topics_absolute_productivity.sum(axis='columns'), axis='rows')
        df_country_topics_relative_productivity['normalization'] = normalization
        return df_country_topics_relative_productivity
    elif normalization == 'global':
        df_country_topics_relative_productivity = df_country_topics_absolute_productivity.div(
            df_country_topics_absolute_productivity.groupby('year').sum(), axis='rows')
        df_country_topics_relative_productivity['normalization'] = normalization
        return df_country_topics_relative_productivity
    elif normalization == 'both':
        df_productivity_global = df_country_topics_absolute_productivity.div(
            df_country_topics_absolute_productivity.sum(axis='columns'), axis='rows')
        df_productivity_global['normalization'] = 'global'
        df_productivity_local = df_country_topics_absolute_productivity.div(
            df_country_topics_absolute_productivity.sum(axis='columns'), axis='rows')
        df_productivity_local['normalization'] = 'local'
        return pd.concat([df_productivity_global, df_productivity_local])
    else:
        raise ValueError("normalization can be set only to 'local', 'global', 'both', 'None'")


def main():
    path_of_files = "../../data/research_papers/one_folder_metadata"
    path_of_topics_csv = "doc_topics.csv"

    df_art, df_aff = df_manipulation.new_create_articles_dfs(path_of_files)
    # print(df_art)
    # print(df_aff)
    df_topics = df_manipulation.create_topics_df(path_of_topics_csv)

    # print(df_aff)

    # l = df_aff.index.get_level_values('affiliation').values
    # print(l)
    # df2 = df_aff.groupby('affiliation').nunique()#['author'].nunique()
    # df2 = df_aff.reset_index().groupby('article').nunique()[['affiliation']]  # ['author'].nunique()
    # print("\n\n\n")
    # print(df2)
    # df3 = df_aff.groupby('affiliation').size()
    # print("\n\n\n")
    # print(df3)

    # df_prod_glob = productivity_country_per_topic(df_aff, df_topics, normalization='global')
    # df_prod_loc = productivity_country_per_topic(df_aff, df_topics, normalization='local')
    # df_prod.to_csv("df_prod.csv", index=True, header=True)
    # df_tot = pd.concat([df_prod_glob, df_prod_loc])#, keys=['global', 'local'])
    # print(df_tot)
    # print(df_prod_glob.merge(df_prod_loc, on='normalization'))
    df_tot = productivity_country_per_topic(df_aff, df_topics, normalization='country_indipendent')
    print(df_tot.query("iso_a3 == 'USA'"))


if __name__ == '__main__':
    main()
