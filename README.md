# Shopping basket

Shopping basket pricing library for a supermarket.

## Design

Composition is used to construct a pricer component with a basket, catalogue and list of offers.

```python
@dataclass
class Pricer:
    basket: Basket
    catalogue: Catalogue
    offers: List[Offer]
```

In order to allow complex offers to be applied the basket must be transformed into a list of price stubs consisting of products and their current prices.

```python
> pricer = Pricer(
     Basket({"apple": 2, "orange": 1}),
     Catalogue({"apple": 1.0, "orange": 2.0})
  )

> pricer.stubs_list
[
    PriceStub(name='apple', price=1.0),
    PriceStub(name='apple', price=1.0),
    PriceStub(name='orange', price=2.0),
]
```

Offers can be applied to update the final price of each product.

```python
def half_price_oranges(stubs_list: List[PriceStub]) -> List[PriceStub]:
    return [
        PriceStub(i.name, i.price / 2 if i.name == "orange" else i.price)
        for i in stubs_list
    ]

> offer = Offer("Half price oranges", half_price_oranges)

> offer.transform(pricer.stubs_list)
[
    PriceStub(name='apple', price=1.0),
    PriceStub(name='apple', price=1.0),
    PriceStub(name='orange', price=1.0),
]
```

This design allows the design of offers to be totally encapsulated by their instances.

```python
T = TypeVar("T")
Transform = Callable[[T], T]

@dataclass
class Offer:
    title: str
    transform: Transform[List[PriceStub]]
```

## Installing

Black is used to format this repository. Since its packages are still pre-releases we must use pipenv's --pre flag to install dependencies.

```bash
pipenv install --pre
```

For the convenience of grouping tooling jobs grunt is used as a task runner.

```bash
npm i
```

## Tooling

To run all unit and bdd tests:

```bash
grunt test
```

To run linters:

```bash
grunt lint
```

To run formatters:

```bash
grunt format
```

## Docs

Google style docstrings are used to document this repository. Full documentation can be generated with sphinx-autodoc and sphinx-apidoc.

## Tests

Unit tests are not enough to capture the desired behavior of the pricer in a readable way. Therefore we include some bdd tests. Scenarios are documented in feature files:

```feature
Feature: Pricer
    Scenario Outline: Pricing a basket with multiple items and offers.
        Given I have a basket with <apples> apples and <oranges> oranges.
        And Apples cost 1.0 and oranges cost 2.0.
        When apples are buy one get one free.
        And oranges are half price.
        Then The sub_total price should be <sub_total>.
        And A discount of <discount> should be applied.
        And The total price should be <total>.

        Examples Vertical:
        | apples    | 1   | 1   | 1   | 2   | 2   | 2   | 3   | 3   | 3   |
        | oranges   | 1   | 2   | 3   | 1   | 2   | 3   | 1   | 2   | 3   |
        | sub_total | 3.0 | 5.0 | 7.0 | 4.0 | 6.0 | 8.0 | 5.0 | 7.0 | 9.0 |
        | discount  | 1.0 | 2.0 | 3.0 | 2.0 | 3.0 | 4.0 | 2.0 | 4.0 | 4.0 |
        | total     | 2.0 | 3.0 | 4.0 | 2.0 | 3.0 | 4.0 | 3.0 | 4.0 | 5.0 |

```

## Remarks

Lots of love to the open source community!

![Be kind][be_kind]

<!-- Links -->

[be_kind]: https://media.giphy.com/media/osAcIGTSyeovPq6Xph/giphy.gif
