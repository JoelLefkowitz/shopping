# Shopping

Shopping basket pricing library for a supermarket.

![Review](https://img.shields.io/github/actions/workflow/status/JoelLefkowitz/shopping/review.yml)
![Version](https://img.shields.io/pypi/v/shopping)
![Downloads](https://img.shields.io/pypi/dw/shopping)
![Quality](https://img.shields.io/codacy/grade/b76ffbb49ba941aaacf8e723292934ef)
![Coverage](https://img.shields.io/codacy/coverage/b76ffbb49ba941aaacf8e723292934ef)

## Installation

```bash
pip install shopping
```

## Documentation

Documentation and more detailed examples are hosted on [Github Pages](https://joellefkowitz.github.io/shopping).

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

## Tooling

### Dependencies

To install dependencies:

```bash
yarn install
pip install .[all]
```

### Tests

To run tests:

```bash
thx test
```

### Documentation

To generate the documentation locally:

```bash
thx docs
```

### Linters

To run linters:

```bash
thx lint
```

### Formatters

To run formatters:

```bash
thx format
```

## Contributing

Please read this repository's [Code of Conduct](CODE_OF_CONDUCT.md) which outlines our collaboration standards and the [Changelog](CHANGELOG.md) for details on breaking changes that have been made.

This repository adheres to semantic versioning standards. For more information on semantic versioning visit [SemVer](https://semver.org).

Bump2version is used to version and tag changes. For example:

```bash
bump2version patch
```

### Contributors

- [Joel Lefkowitz](https://github.com/joellefkowitz) - Initial work

## Remarks

Lots of love to the open source community!

<div align='center'>
    <img width=200 height=200 src='https://media.giphy.com/media/osAcIGTSyeovPq6Xph/giphy.gif' alt='Be kind to your mind' />
    <img width=200 height=200 src='https://media.giphy.com/media/KEAAbQ5clGWJwuJuZB/giphy.gif' alt='Love each other' />
    <img width=200 height=200 src='https://media.giphy.com/media/WRWykrFkxJA6JJuTvc/giphy.gif' alt="It's ok to have a bad day" />
</div>
