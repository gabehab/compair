import trueskill

from compair.algorithms.score.score_algorithm_base import ScoreAlgorithmBase
from compair.algorithms.comparison_pair import ComparisonPair
from compair.algorithms.comparison_winner import ComparisonWinner
from compair.algorithms.scored_object import ScoredObject

from compair.algorithms.exceptions import InvalidWinnerException

class TrueSkillAlgorithmWrapper(ScoreAlgorithmBase):
    def __init__(self):
        ScoreAlgorithmBase.__init__(self)

        # storage[key] = ScoredObject
        self.storage = {}
        # storage[key] = set() of opponent keys
        self.opponents = {}
        # storage[key] = true skill rating object
        self.ratings = {}

    def calculate_score_1vs1(self, key1_scored_object, key2_scored_object, winner, other_comparison_pairs):
        """
        Calculates the scores for a new 1vs1 comparison without re-calculating all previous scores
        :param key1_scored_object: Contains score parameters for key1
        :param key2_scored_object: Contains score parameters for key2
        :param winner: indicates comparison winner
        :param other_comparison_pairs: Contains all previous comparison_pairs that the 2 keys took part in.
            This is a subset of all comparison pairs and is used to calculate round, wins, loses, and opponent counts
        :return: tuple of ScoredObject (key1, key2)
        """
        self.storage = {}
        self.opponents = {}
        self.ratings = {}
        trueskill.setup()

        key1 = key1_scored_object.key
        key2 = key2_scored_object.key

        # Note: if value are None, trueskill.Rating will use default mu 25 and sigma 8.333
        r1 = trueskill.Rating(
            mu=key1_scored_object.variable1,
            sigma=key1_scored_object.variable2
        )

        r2 = trueskill.Rating(
            mu=key2_scored_object.variable1,
            sigma=key2_scored_object.variable2
        )

        if winner == ComparisonWinner.key1:
            r1, r2 = trueskill.rate_1vs1(r1, r2)
        elif winner == ComparisonWinner.key2:
            r2, r1 = trueskill.rate_1vs1(r2, r1)
        elif winner == ComparisonWinner.draw:
            r1, r2 = trueskill.rate_1vs1(r1, r2, drawn=True)
        else:
            raise InvalidWinnerException

        self.ratings[key1] = r1
        self.ratings[key2] = r2

        for key in [key1, key2]:
            self.opponents[key] = set()
            self.storage[key] = ScoredObject(
                key=key,
                score=trueskill.expose(self.ratings[key]),
                variable1=self.ratings[key].mu,
                variable2=self.ratings[key].sigma,
                rounds=0,
                opponents=0,
                wins=0,
                loses=0
            )

        # calculate opponents, wins, loses, rounds for every match for key1 and key2
        for comparison_pair in (other_comparison_pairs + [ComparisonPair(key1, key2, winner)]):
            cp_key1 = comparison_pair.key1
            cp_key2 = comparison_pair.key2
            cp_winner = comparison_pair.winner
            cp_key1_winner = cp_winner == ComparisonWinner.key1
            cp_key2_winner = cp_winner == ComparisonWinner.key2

            if cp_key1 == key1 or cp_key1 == key2:
                if cp_winner is None:
                    self._update_rounds_only(cp_key1)
                else:
                    self._update_result_stats(cp_key1, cp_key2, cp_key1_winner, cp_key2_winner)

            if cp_key2 == key1 or cp_key2 == key2:
                if cp_winner is None:
                    self._update_rounds_only(cp_key2)
                else:
                    self._update_result_stats(cp_key2, cp_key1, cp_key2_winner, cp_key1_winner)

        return (self.storage[key1], self.storage[key2])

    def calculate_score(self, comparison_pairs):
        """
        Calculate scores for a set of comparison_pairs
        :param comparison_pairs: array of comparison_pairs
        :return: dictionary key -> ScoredObject
        """
        self.storage = {}
        self.opponents = {}
        self.ratings = {}
        trueskill.setup()

        keys = self.get_keys_from_comparison_pairs(comparison_pairs)
        # create default ratings for every available key
        for key in keys:
            rating = trueskill.Rating()
            self.ratings[key] = rating
            self.opponents[key] = set()

            self.storage[key] = ScoredObject(
                key=key,
                score=trueskill.expose(rating),
                variable1=rating.mu,
                variable2=rating.sigma,
                rounds=0,
                opponents=0,
                wins=0,
                loses=0
            )

        # calculate rating by for every match
        for comparison_pair in comparison_pairs:
            key1 = comparison_pair.key1
            key2 = comparison_pair.key2
            winner = comparison_pair.winner

            # skip incomplete comparisosns
            if winner is None:
                self._update_rounds_only(key1)
                self._update_rounds_only(key2)
                continue

            r1 = self.ratings[key1]
            r2 = self.ratings[key2]

            key1_winner = winner == ComparisonWinner.key1
            key2_winner = winner == ComparisonWinner.key2

            if key1_winner:
                r1, r2 = trueskill.rate_1vs1(r1, r2)
            elif key2_winner:
                r2, r1 = trueskill.rate_1vs1(r2, r1)
            elif winner == ComparisonWinner.draw:
                r1, r2 = trueskill.rate_1vs1(r1, r2, drawn=True)
            else:
                raise InvalidWinnerException

            self._update_rating(key1, r1, key2, key1_winner, key2_winner)
            self._update_rating(key2, r2, key1, key2_winner, key1_winner)

        # return comparison results
        return self.storage

    def _update_rounds_only(self, key):
        rounds = self.storage[key].rounds
        self.storage[key] = self.storage[key]._replace(rounds=rounds+1)

    def _update_result_stats(self, key, opponent_key, did_win, did_lose):
        self.opponents[key].add(opponent_key)
        wins = self.storage[key].wins
        loses = self.storage[key].loses

        # winner == None should not increase total wins or loses
        self.storage[key] = ScoredObject(
            key=key,
            score=self.storage[key].score,
            variable1=self.ratings[key].mu,
            variable2=self.ratings[key].sigma,
            rounds=self.storage[key].rounds+1,
            opponents=len(self.opponents[key]),
            wins=wins+1 if did_win else wins,
            loses=loses+1 if did_lose else loses,
        )

    def _update_rating(self, key, new_rating, opponent_key, did_win, did_lose):
        self.ratings[key] = new_rating
        self.opponents[key].add(opponent_key)
        wins = self.storage[key].wins
        loses = self.storage[key].loses

        # winner == None should not increase total wins or loses
        self.storage[key] = ScoredObject(
            key=key,
            score=trueskill.expose(new_rating),
            variable1=new_rating.mu,
            variable2=new_rating.sigma,
            rounds=self.storage[key].rounds+1,
            opponents=len(self.opponents[key]),
            wins=wins+1 if did_win else wins,
            loses=loses+1 if did_lose else loses,
        )

