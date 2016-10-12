import unittest

from setgame import SetBoard, SetCard, SetDeck, SetHand
from setgame import SetColor, SetShading, SetShape

class TestSetGameBoard(unittest.TestCase):

    def setUp(self):
        self.deck = SetDeck()

        # "System Under Test," i.e., the board:
        self.SUT = SetBoard(self.deck)

        self.card1 = SetCard(
            count=1,
            color=SetColor.red,
            shading=SetShading.empty,
            shape=SetShape.squiggles
        )

        self.card2 = SetCard(
            count=2,
            color=SetColor.green,
            shading=SetShading.striped,
            shape=SetShape.oval
        )

    def contrive_no_match_in_deck(self):
        # Force a deal-out from the deck to return this hand
        # that does not make a valid set:
        self.card3 = SetCard(
            count=3,
            color=SetColor.purple,
            shading=SetShading.solid,
            shape=SetShape.oval
        )
        self.encoding1 = self.card1.encoding
        self.encoding2 = self.card2.encoding
        self.encoding3 = self.card3.encoding

        non_matching_hand = SetHand(self.card1, self.card2, self.card3)
        self.assertFalse(non_matching_hand.is_set())

        self.deck.cards_by_encoding = {
            self.encoding1: self.card1,
            self.encoding2: self.card2,
            self.encoding3: self.card3
        }

    def test_board_init_leaves_cards_be(self):
        self.assertEqual(81, len(self.deck.cards))
        self.assertEqual(0, len(self.SUT.cards))

    def test_board_setup_uniquely_puts_cards_on_board(self):
        self.SUT.setup()

        self.assertEqual(12, len(self.SUT.cards))
        self.assertEqual(69, len(self.deck.cards))

        for card in self.SUT.cards_by_encoding:
            self.assertNotIn(card, self.deck.cards_by_encoding)

    def test_board_draw_from_deck_draws_uniquely(self):
        card = self.SUT.draw_from_deck()

        self.assertEqual(card, self.SUT.cards_by_encoding[card.encoding])
        self.assertEqual(80, len(self.deck.cards))
        self.assertNotIn(card, self.deck.cards)

    def test_board_derives_third_encoding_in_set(self):
        encoding1 = self.card1.encoding
        encoding2 = self.card2.encoding

        card3 = SetCard(
            count=3,
            color=SetColor.purple,
            shading=SetShading.solid,
            shape=SetShape.diamond
        )
        encoding3 = card3.encoding

        # These all make a set:
        hand = SetHand(self.card1, self.card2, card3)
        self.assertTrue(hand.is_set())

        generated_third_encoding = SetBoard.missing_encoding_from(
            encoding1,
            encoding2
        )

        self.assertEqual(encoding3, generated_third_encoding)

    def test_board_remove_set_rolls_back_if_some_key_does_not_exist_in_board(self):
        encoding1 = self.card1.encoding
        encoding2 = self.card2.encoding
        self.SUT.cards_by_encoding[encoding1] = self.card1
        self.SUT.cards_by_encoding[encoding2] = self.card2

        card3 = SetCard(
            count=3,
            color=SetColor.purple,
            shading=SetShading.solid,
            shape=SetShape.diamond
        )
        encoding3 = card3.encoding

        with self.assertRaises(KeyError):
            self.SUT.remove_set(encoding1, encoding2, encoding3)

        self.assertEqual(2, len(self.SUT.cards))
        self.assertEqual(0, len(self.SUT.graveyard))

    def test_board_remove_set_returns_SetHand_of_denoted_cards(self):
        encoding1 = self.card1.encoding
        encoding2 = self.card2.encoding

        card3 = SetCard(
            count=3,
            color=SetColor.purple,
            shading=SetShading.solid,
            shape=SetShape.diamond
        )
        encoding3 = card3.encoding

        self.SUT.cards_by_encoding = {
            encoding1: self.card1,
            encoding2: self.card2,
            encoding3: card3
        }

        hand = self.SUT.remove_set(encoding1, encoding2, encoding3)

        for card in (self.card1, self.card2, card3):
            self.assertIn(card, hand.cards)

    def test_board_find_set_returns_None_if_no_set_and_adds_to_waitlist(self):
        self.contrive_no_match_in_deck()

        # Move from the deck to the board:
        for i in self.deck.cards:
            self.SUT.draw_from_deck()

        self.assertIsNone(self.SUT.find_set())

        missing_encoding = SetBoard.missing_encoding_from(self.encoding1, self.encoding2)
        partners = self.SUT.waitlist[missing_encoding][0]
        self.assertIn(self.encoding1, partners)
        self.assertIn(self.encoding2, partners)

        missing_encoding = SetBoard.missing_encoding_from(self.encoding2, self.encoding3)
        partners = self.SUT.waitlist[missing_encoding][0]
        self.assertIn(self.encoding2, partners)
        self.assertIn(self.encoding3, partners)

        missing_encoding = SetBoard.missing_encoding_from(self.encoding1, self.encoding3)
        partners = self.SUT.waitlist[missing_encoding][0]
        self.assertIn(self.encoding1, partners)
        self.assertIn(self.encoding3, partners)

    def test_board_find_set_returns_hand_and_moves_cards_into_graveyard(self):
        encoding1 = self.card1.encoding
        encoding2 = self.card2.encoding
        card3 = SetCard(
            count=3,
            color=SetColor.purple,
            shading=SetShading.solid,
            shape=SetShape.diamond
        )
        encoding3 = card3.encoding

        hand = SetHand(self.card1, self.card2, card3)
        self.assertTrue(hand.is_set())

        self.SUT.cards_by_encoding = {
            encoding1: self.card1,
            encoding2: self.card2,
            encoding3: card3
        }

        returned_hand = self.SUT.find_set()

        self.assertTrue(returned_hand.is_set())

        self.assertEqual(0, len(self.SUT.cards))
        self.assertIs(self.card1, self.SUT.graveyard_by_encoding[encoding1])
        self.assertIs(self.card2, self.SUT.graveyard_by_encoding[encoding2])
        self.assertIs(card3, self.SUT.graveyard_by_encoding[encoding3])

    def test_board_add_to_waitlist_creates_new_entry_in_waitlist(self):
        encoding1 = self.card1.encoding
        encoding2 = self.card2.encoding

        encoding3 = SetBoard.missing_encoding_from(encoding1, encoding2)

        self.assertNotIn(encoding3, self.SUT.waitlist)

        self.SUT.add_to_waitlist(encoding3, encoding1, encoding2)

        partners = self.SUT.waitlist[encoding3][0]

        self.assertIn(encoding1, partners)
        self.assertIn(encoding2, partners)

    def test_board_find_set_handles_duplicate_waitlist_entries(self):
        # 0000 = 0 red solid diamond, 1
        # --------
        # 0001 = 1 red solid diamond, 2
        # 0002 = 2 red solid diamond, 3
        # --------
        # 0010 = 3 red solid squiggles, 1
        # 0020 = 6 red solid oval, 1
        # --------
        # 0100 = 9 red empty diamond, 1
        # 0200 = 18 red striped diamond, 1

        missing_card = SetCard(
            color=SetColor.red,
            shading=SetShading.solid,
            shape=SetShape.diamond,
            count=1
        )
        missing_encoding = missing_card.encoding
        self.assertEqual(0, missing_encoding)

        # -----------------------------------------

        card1 = SetCard(
            color=SetColor.red,
            shading=SetShading.solid,
            shape=SetShape.diamond,
            count=2
        )
        encoding1 = card1.encoding
        self.assertEqual(1, encoding1)

        card2 = SetCard(
            color=SetColor.red,
            shading=SetShading.solid,
            shape=SetShape.diamond,
            count=3
        )
        encoding2 = card2.encoding
        self.assertEqual(2, encoding2)

        missing_1_2 = SetBoard.missing_encoding_from(encoding1, encoding2)
        self.assertEqual(missing_encoding, missing_1_2)

        self.SUT.add_to_waitlist(missing_encoding, encoding1, encoding2)

        # ------------------------------------------

        card3 = SetCard(
            color=SetColor.red,
            shading=SetShading.solid,
            shape=SetShape.squiggles,
            count=1
        )
        encoding3 = card3.encoding
        self.assertEqual(3, encoding3)

        card4 = SetCard(
            color=SetColor.red,
            shading=SetShading.solid,
            shape=SetShape.oval,
            count=1
        )
        encoding4 = card4.encoding
        self.assertEqual(6, encoding4)

        missing_3_4 = SetBoard.missing_encoding_from(encoding3, encoding4)
        self.assertEqual(missing_encoding, missing_3_4)

        self.SUT.add_to_waitlist(missing_encoding, encoding3, encoding4)

        # -------------------------------------------

        card5 = SetCard(
            color=SetColor.red,
            shading=SetShading.empty,
            shape=SetShape.diamond,
            count=1
        )
        encoding5 = card5.encoding
        self.assertEqual(9, encoding5)

        card6 = SetCard(
            color=SetColor.red,
            shading=SetShading.striped,
            shape=SetShape.diamond,
            count=1
        )
        encoding6 = card6.encoding
        self.assertEqual(18, encoding6)

        missing_5_6 = SetBoard.missing_encoding_from(encoding5, encoding6)
        self.assertEqual(missing_encoding, missing_5_6)

        self.SUT.add_to_waitlist(missing_encoding, encoding5, encoding6)

        # ===========================================

        # Check waitlist:
        partner_sets = self.SUT.waitlist[missing_encoding]
        self.assertIn(set([encoding1, encoding2]), partner_sets)
        self.assertIn(set([encoding3, encoding4]), partner_sets)
        self.assertIn(set([encoding5, encoding6]), partner_sets)

        # Clear waitlist so we can test that this behavior is
        # preserved through find_set:
        self.SUT.waitlist = {}

        self.SUT.cards_by_encoding = {
            encoding1: card1,
            encoding2: card2,
            encoding3: card3,
            encoding4: card4,
            encoding5: card5,
            encoding6: card6
        }

        found_set = self.SUT.find_set()

        self.assertIsNone(found_set)

        # Check waitlist:
        partner_sets = self.SUT.waitlist[missing_encoding]
        self.assertIn(set([encoding1, encoding2]), partner_sets)
        self.assertIn(set([encoding3, encoding4]), partner_sets)
        self.assertIn(set([encoding5, encoding6]), partner_sets)

    def test_board_deal_and_search_returns_immediately_if_new_cards_make_set(self):
        encoding1 = self.card1.encoding
        encoding2 = self.card2.encoding
        card3 = SetCard(
            count=3,
            color=SetColor.purple,
            shading=SetShading.solid,
            shape=SetShape.diamond
        )
        encoding3 = card3.encoding

        expected_hand = SetHand(self.card1, self.card2, card3)
        self.assertTrue(expected_hand.is_set())

        # Force a deal-out from the deck to return this matching set:
        self.deck.cards_by_encoding = {
            encoding1: self.card1,
            encoding2: self.card2,
            encoding3: card3
        }

        # These existing cards would make a set with card1:
        card4 = SetCard(
            count=2,
            color=SetColor.red,
            shading=SetShading.empty,
            shape=SetShape.squiggles
        )
        card5 = SetCard(
            count=3,
            color=SetColor.red,
            shading=SetShading.empty,
            shape=SetShape.squiggles
        )

        self.SUT.cards_by_encoding = {
            card4.encoding: card4,
            card5.encoding: card5
        }

        would_be_hand = SetHand(self.card1, card4, card5)
        self.assertTrue(would_be_hand.is_set())

        new_hand = self.SUT.deal_and_search()

        self.assertTrue(new_hand.is_set())

        self.assertEqual(3, len(self.SUT.graveyard))
        for enc in (encoding1, encoding2, encoding3):
            self.assertIn(enc, self.SUT.graveyard_by_encoding)

        self.assertEqual(2, len(self.SUT.cards))
        for enc in (card4.encoding, card5.encoding):
            self.assertIn(enc, self.SUT.cards_by_encoding)

    def test_board_deal_search_returns_hand_based_on_waitlist_and_updates(self):
        self.contrive_no_match_in_deck()

        # Existing cards whose missing third is card3:
        existing_card1 = SetCard(
            count=1,
            color=SetColor.purple,
            shading=SetShading.solid,
            shape=SetShape.oval
        )
        existing_encoding1 = existing_card1.encoding

        existing_card2 = SetCard(
            count=2,
            color=SetColor.purple,
            shading=SetShading.solid,
            shape=SetShape.oval
        )
        existing_encoding2 = existing_card2.encoding

        generated_encoding3 = SetBoard.missing_encoding_from(
            existing_encoding1,
            existing_encoding2
        )
        self.assertEqual(self.encoding3, generated_encoding3)

        self.SUT.cards_by_encoding = {
            existing_encoding1: existing_card1,
            existing_encoding2: existing_card2
        }

        # Set up waitlist:
        self.SUT.add_to_waitlist(self.encoding3, existing_encoding1, existing_encoding2)

        # Deal in new cards and expect that card3 was found in the
        # waitlist:
        matching_hand = self.SUT.deal_and_search()
        self.assertTrue(matching_hand.is_set())

        for card in (self.card3, existing_card1, existing_card2):
            self.assertIn(card, matching_hand.cards)
            self.assertIn(card, self.SUT.graveyard)
            self.assertNotIn(card, self.SUT.cards)

    def test_board_deal_and_search_matches_two_new_cards_to_existing_card(self):
        self.contrive_no_match_in_deck()
