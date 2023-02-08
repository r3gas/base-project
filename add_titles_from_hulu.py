from hulu_bot.hulu_session import HuluSession


if __name__ == "__main__":
    # Creates instance of Hulu session
    session = HuluSession()
    session.login('{email}', '{password}', '{profile_name}')
    session.navigate_to_movie_tab()
    session.get_movie_tab_titles()


