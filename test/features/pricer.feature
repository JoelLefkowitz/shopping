Feature: Pricer

    Scenario Outline: Pricing a basket with multiple items and offers.
        Given I have a basket with <apples> apples and <oranges> oranges.
        And Apples cost 1.0 and oranges cost 2.0.
        When Apples are buy one get one free.
        And Oranges are half price.
        Then The sub_total price should be <sub_total>.
        And A discount of <discount> should be applied.
        And The total price should be <total>.

        Examples: Vertical
        | apples    | 1   | 1   | 1   | 2   | 2   | 2   | 3   | 3   | 3   |
        | oranges   | 1   | 2   | 3   | 1   | 2   | 3   | 1   | 2   | 3   |
        | sub_total | 3.0 | 5.0 | 7.0 | 4.0 | 6.0 | 8.0 | 5.0 | 7.0 | 9.0 |
        | discount  | 1.0 | 2.0 | 3.0 | 2.0 | 3.0 | 4.0 | 2.0 | 4.0 | 4.0 |
        | total     | 2.0 | 3.0 | 4.0 | 2.0 | 3.0 | 4.0 | 3.0 | 4.0 | 5.0 |
