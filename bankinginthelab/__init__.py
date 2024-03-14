from otree.api import *
import random
import pandas as pd
import numpy as np





doc = """
This is a banking in the lab experiment built based on the microfounded model in 
Gu, C., Mattesini, F., Monnet, C., & Wright, R. (2013). Banking: A new monetarist approach. Review of Economic Studies, 80(2), 636-662.
"""


class C(BaseConstants):
    NAME_IN_URL = 'bankinginthelab'
    PLAYERS_PER_GROUP = 2

    ### determine the length of the experiments ###
    MAX_ROUND = 30
    DESIRED_ROUND_LENGTH = 10
    TERMINATING_ROLL = 10
    ROUND_TERMINATION_ROLLS = [0 for i in range(MAX_ROUND)]
    for i in range(len(ROUND_TERMINATION_ROLLS)):
        ROUND_TERMINATION_ROLLS[i] = random.randint(1,10)

    # 11 PERIODS, seq1
    # ROUND_TERMINATION_ROLLS = [2, 9, 2, 4, 1, 3, 2, 8, 9, 1, 2, 10, 1, 8, 10, 8, 3, 7, 4, 7, 2, 2, 6, 4, 8, 10, 10, 6, 5, 9]
    # 10 PERIODS, seq2
    # ROUND_TERMINATION_ROLLS = [4, 7, 4, 8, 5, 4, 1, 10, 6, 4, 6, 8, 8, 4, 8, 9, 4, 4, 5, 9, 1, 2, 7, 8, 1, 7, 7, 7, 7, 9]
    # 10 PERIODS, seq3
    ROUND_TERMINATION_ROLLS = [9, 8, 2, 8, 2, 4, 4, 5, 10, 10, 4, 6, 10, 4, 8, 10, 4, 1, 5, 10, 1, 7, 4, 5, 2, 5, 4, 9, 4, 2]
    if TERMINATING_ROLL in ROUND_TERMINATION_ROLLS[0:DESIRED_ROUND_LENGTH]:
        NUM_ROUNDS = 10
        for i in range(DESIRED_ROUND_LENGTH):
            if ROUND_TERMINATION_ROLLS[i] == TERMINATING_ROLL:
                NUM_ROUNDS_SHADOW = i
    else:
        for i in range(DESIRED_ROUND_LENGTH,len(ROUND_TERMINATION_ROLLS)):
            if TERMINATING_ROLL in ROUND_TERMINATION_ROLLS[DESIRED_ROUND_LENGTH:len(ROUND_TERMINATION_ROLLS)]:
                if ROUND_TERMINATION_ROLLS[i] == TERMINATING_ROLL:
                    NUM_ROUNDS = i
                    break
            else:
                NUM_ROUNDS = MAX_ROUND
    print(NUM_ROUNDS)
    print(ROUND_TERMINATION_ROLLS)

    ### END - determine the length of the experiments ###

    INSTRUCTIONS_TEMPLATE = 'bankinginthelab/instructions.html'


    UTILITY_PARAMETER = 2
    RHO = 1.2 #gross investment return when type 1 invest y
    LAMBDA = 0.5 #reneging benefit (of type 1)

    TYPE1_ENDOWMENT = 1
    TYPE2_ENDOWMENT = 1  # NOTE: THE CODE WORKS IFF BOTH ENDOWMENTS EQUALIZED, IF NOT NEED MODIFIES
    MAX_SCORE = 3
    SCORE_SCALE = 100

    EXCHANGE_RATE = 0.9



    ROUND_TERMINATION_INTEGER = 10

class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    subsession.group_randomly(fixed_id_in_group=True)

class Group(BaseGroup):

    ## QUIZ QUESTION (PRE-EXPERIMENT)
    quiz1 = models.IntegerField(
        choices = [
            [0, 'a. Good Y, produced by you'],
            [1, 'b. Good X, produced by a type 2 participant'],
            [0, 'c. Good X, produced by you'],
        ],
        widget=widgets.RadioSelect,
        label='If you are a type 1, which type of good that you can earn points by obtaining?',
    )

    quiz2 = models.IntegerField(
        choices=[
            [0, 'a. Produce and Transfer 1 unit of good Y to your partner being type 1'],
            [0, 'b. Produce and Invest 1 unit of good X for your partner being type 1'],
            [1, 'c. Produce and Transfer 1 unit of good X to your partner being type 1'],
        ],
        widget=widgets.RadioSelect,
        label='If you are a type 2, what is your proposed action in stage 1?',
    )

    quiz3 = models.IntegerField(
        choices=[
            [0, 'a. 140'],
            [0, 'b. 0'],
            [1, 'c. -100'],
        ],
        widget=widgets.RadioSelect,
        label='If you are a type 2, what are your earnings in a round if your partner does not transfer their production to you in stage 2 (except the first round)?',
    )

    quiz4 = models.IntegerField(
        choices=[
            [1, 'a. 100 if transfer, 160 if does not transfer'],
            [0, 'b. 0 if transfer, 160 if does not transfer'],
            [0, 'c. 100 if transfer, 100 if does not transfer'],
        ],
        widget=widgets.RadioSelect,
        label='If you are a type 1, what are your earnings in a round if you transfer the production to your partner in stage 2? and what if you do not (except the first round)?',
    )

    stage1_type1_decision = models.IntegerField(
        choices = [[0, 'Do not accept'],[1, 'Accept']],
        doc = """Type 1's production decision (stage 1)""",
        widget=widgets.RadioSelect,
        label = 'Do you accept the proposed action?',
        # label = "The planner recommend that you produce (at a cost of)"
        initial = 2
    )

    stage1_type2_decision = models.IntegerField(
        choices=[[0, 'Do not accept'], [1, 'Accept']],
        doc="""Type 2's production decision""",
        widget=widgets.RadioSelect,
        label = 'Do you accept the proposed action?',
        # label="The planner recommend that you produce (at a cost of)"
        initial = 2
    )

    stage2_type1_decision = models.IntegerField(
        choices=[[0, 'No'], [1, 'Yes']],
        doc="""Type 1's delivery decision (stage 2)""",
        widget=widgets.RadioSelect,
        label = '',
        initial = 2
        # label="Do you wish to deliver the production of good y to your partner?"
    )


    stage1_partnership = models.IntegerField(min=0,initial=0)
    stage2_delivery = models.IntegerField(min=0,initial=0)



    # score = models.FloatField(min=0,initial=0)
    # cum_score = models.FloatField(min=0,initial=0)

class Player(BasePlayer):
    score = models.FloatField(initial = C.TYPE1_ENDOWMENT*C.SCORE_SCALE)
    cum_score = models.FloatField(initial=C.TYPE1_ENDOWMENT*C.SCORE_SCALE)
    round_termination = models.IntegerField(min=1, initial=1)

    exclusion_marking = models.IntegerField(min=0, initial=0)


# FUNCTIONS
def compute_partnership_outcome(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    if group.field_maybe_none('stage1_type1_decision') == 1 and group.field_maybe_none('stage1_type2_decision') == 1:
        group.stage1_partnership = 1
    else:
        group.stage1_partnership = 0

def compute_delivery_outcome(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    if group.field_maybe_none('stage2_type1_decision') == 1:
        group.stage2_delivery = 1
    else:
        group.stage2_delivery = 0

def set_payoffs_stage1(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    round = group.subsession.round_number
    if round == 1:
        p1.score = C.TYPE1_ENDOWMENT * C.SCORE_SCALE
        p2.score = C.TYPE2_ENDOWMENT * C.SCORE_SCALE
    else:
        p1.score = 0
        p2.score = 0
    if group.stage1_partnership == 1:
        p1.score = p1.score + (C.UTILITY_PARAMETER*(C.TYPE1_ENDOWMENT)**(1/2) - C.TYPE1_ENDOWMENT)* C.SCORE_SCALE
        p2.score = p2.score - (C.TYPE2_ENDOWMENT)* C.SCORE_SCALE
    else:
        p1.score = p1.score
        p2.score = p2.score

    if round == 1:
        p1.cum_score = p1.score
        p2.cum_score = p2.score
    else:
        p1.cum_score = p1.score + p1.in_previous_rounds()[-1].cum_score
        p2.cum_score = p2.score + p2.in_previous_rounds()[-1].cum_score

def set_payoffs_stage2(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    round = group.subsession.round_number
    if group.stage1_partnership == 1:
        if group.stage2_delivery == 1:
            p1.score = p1.score
            p2.score = p2.score + (C.RHO*C.UTILITY_PARAMETER*(C.TYPE1_ENDOWMENT)**(1/2))* C.SCORE_SCALE
        else:
            p1.score = p1.score + (C.LAMBDA*C.RHO*(C.TYPE2_ENDOWMENT))* C.SCORE_SCALE
            p2.score = p2.score
    else:
        p1.score = p1.score
        p2.score = p2.score

    if round == 1:
        p1.cum_score = p1.score
        p2.cum_score = p2.score
    else:
        p1.cum_score = p1.score + p1.in_previous_rounds()[-1].cum_score
        p2.cum_score = p2.score + p2.in_previous_rounds()[-1].cum_score

# def type1_decisions_automation(group: Group):
#     group.field_maybe_none('stage1_type1_decision') = 0
#     group.field_maybe_none('stage2_type1_decision') = 1
#
# def exclusion_marking(group: Group):
#     group.field_maybe_none('exclusion_marking') = 1
#
# def type2_decisions_automation(group: Group):
#     group.field_maybe_none('stage1_type2_decision') = 0







######### PAGES #########
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

class Intro_waitpage(WaitPage):
    pass

class Quiz(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

    form_model = 'group'
    form_fields = ['quiz1','quiz2','quiz3','quiz4']

    @staticmethod
    def error_message(group, values):
        if values['quiz1'] + values['quiz2'] + values['quiz3'] + values['quiz4'] != 4:
            return 'There are at least one incorrect answer, please redo the quiz.'

class Type_page(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == 1

    def vars_for_template(player: Player):
        data_dict = {'': ''}
        data_dict['type'] = player.id_in_group
        return data_dict



class Stage1_type1_page(Page):

    form_model = 'group'
    form_fields = ['stage1_type1_decision']

    @staticmethod
    def is_displayed(player: Player):
        if player.subsession.round_number == 1:
            return player.id_in_group == 1
        else:
            return player.id_in_group == 1 and player.in_previous_rounds()[-1].exclusion_marking == 0

    def vars_for_template(player: Player):
        data_dict = {'': ''}
        data_dict['type'] = player.id_in_group
        data_dict['now'] = player.subsession.round_number
        data_dict['yesterday'] = player.subsession.round_number - 1
        data_dict['score'] = round(player.score,2)
        if player.subsession.round_number == 1:
            data_dict['cum_score'] = round(player.score,2)
        else:
            data_dict['cum_score'] = round(player.in_previous_rounds()[-1].cum_score,2)

        ### history table ###
        groups_id = []
        stage1_outcomes = []
        stage2_outcomes = []
        type1_earning = []
        type2_earning = []
        for p in player.subsession.get_players():
            if p.id_in_group == 1:
                groups_id.append(p.group.id_in_subsession)
                if player.subsession.round_number == 1:
                    stage1_outcomes.append(' - ')
                    stage2_outcomes.append(' - ')
                    type1_earning.append(' - ')
                    type2_earning.append(' - ')
                else:
                    if p.in_previous_rounds()[-1].group.stage1_partnership == 1:
                        stage1_outcomes.append('YES')
                        if p.in_previous_rounds()[-1].group.stage2_delivery == 1:
                            stage2_outcomes.append('YES')
                            type1_earning.append(C.TYPE1_ENDOWMENT-C.TYPE1_ENDOWMENT+C.UTILITY_PARAMETER*(C.TYPE2_ENDOWMENT)**(1/2))
                            type2_earning.append(C.TYPE2_ENDOWMENT-C.TYPE2_ENDOWMENT+C.RHO*C.UTILITY_PARAMETER*(C.TYPE1_ENDOWMENT)**(1/2))
                        else:
                            stage2_outcomes.append('NO')
                            type1_earning.append(C.TYPE1_ENDOWMENT - C.TYPE1_ENDOWMENT + 2 * (C.TYPE2_ENDOWMENT) ** (1 / 2)+C.LAMBDA*C.RHO*C.TYPE2_ENDOWMENT)
                            type2_earning.append(C.TYPE2_ENDOWMENT - C.TYPE2_ENDOWMENT)
                    else:
                        stage1_outcomes.append('NO')
                        stage2_outcomes.append(' - ')
                        type1_earning.append(C.TYPE1_ENDOWMENT)
                        type2_earning.append(C.TYPE2_ENDOWMENT)
        groups_id = np.sort(groups_id)
        history_table = {'PARTNERSHIP': groups_id,
                         'TRADE AGREEMENT in STAGE 1': stage1_outcomes,
                         'TYPE 1 TRANSFER in STAGE 2': stage2_outcomes,
                         'TYPE 1 ROUND EARNING': type1_earning,
                         'TYPE 2 ROUND EARNING': type2_earning}
        history_table = pd.DataFrame(history_table, index=groups_id)
        history_table.index.name = "PARTNERSHIP"
        history_table = history_table.to_html(index=False, justify="justify-all")
        data_dict['history_table'] = history_table
        ### END - history table ###

        ### history graph ###
        type1_average_scores = ['-']
        type2_average_scores = ['-']
        for t in range(1, player.subsession.round_number):
            type1_scores = []
            type2_scores = []
            for p in player.subsession.get_players():
                if p.id_in_group == 1:
                    type1_scores.append(p.in_round(t).score)
                if p.id_in_group == 2:
                    type2_scores.append(p.in_round(t).score)
            type1_average_scores.append(round(np.average(type1_scores),2))
            type2_average_scores.append(round(np.average(type2_scores),2))
        data_dict['type1_average_scores'] = (type1_average_scores)
        data_dict['type2_average_score'] = (type2_average_scores)
        ### END - history graph ###

        return data_dict

class Stage1_type2_page(Page):

    form_model = 'group'
    form_fields = ['stage1_type2_decision']

    @staticmethod
    def is_displayed(player: Player):
        if player.subsession.round_number == 1:
            return player.id_in_group == 2
        else:
            return player.id_in_group == 2 and player.group.get_player_by_id(1).in_previous_rounds()[-1].exclusion_marking == 0

    def vars_for_template(player: Player):
        data_dict = {'': ''}
        data_dict['type'] = player.id_in_group
        data_dict['now'] = player.subsession.round_number
        data_dict['yesterday'] = player.subsession.round_number - 1
        data_dict['score'] = round(player.score,2)
        if player.subsession.round_number == 1:
            data_dict['cum_score'] = round(player.score,2)
        else:
            data_dict['cum_score'] = round(player.in_previous_rounds()[-1].cum_score,2)

        ### history table ###
        groups_id = []
        stage1_outcomes = []
        stage2_outcomes = []
        type1_earning = []
        type2_earning = []
        for p in player.subsession.get_players():
            if p.id_in_group == 1:
                groups_id.append(p.group.id_in_subsession)
                if player.subsession.round_number == 1:
                    stage1_outcomes.append(' - ')
                    stage2_outcomes.append(' - ')
                    type1_earning.append(' - ')
                    type2_earning.append(' - ')
                else:
                    if p.in_previous_rounds()[-1].group.stage1_partnership == 1:
                        stage1_outcomes.append('YES')
                        if p.in_previous_rounds()[-1].group.stage2_delivery == 1:
                            stage2_outcomes.append('YES')
                            type1_earning.append(C.TYPE1_ENDOWMENT-C.TYPE1_ENDOWMENT+C.UTILITY_PARAMETER*(C.TYPE2_ENDOWMENT)**(1/2))
                            type2_earning.append(C.TYPE2_ENDOWMENT-C.TYPE2_ENDOWMENT+C.RHO*C.UTILITY_PARAMETER*(C.TYPE1_ENDOWMENT)**(1/2))
                        else:
                            stage2_outcomes.append('NO')
                            type1_earning.append(C.TYPE1_ENDOWMENT - C.TYPE1_ENDOWMENT + 2 * (C.TYPE2_ENDOWMENT) ** (1 / 2)+C.LAMBDA*C.RHO*C.TYPE2_ENDOWMENT)
                            type2_earning.append(C.TYPE2_ENDOWMENT - C.TYPE2_ENDOWMENT)
                    else:
                        stage1_outcomes.append('NO')
                        stage2_outcomes.append(' - ')
                        type1_earning.append(C.TYPE1_ENDOWMENT)
                        type2_earning.append(C.TYPE2_ENDOWMENT)
        groups_id = np.sort(groups_id)
        history_table = {'PARTNERSHIP': groups_id,
                         'TRADE AGREEMENT in STAGE 1': stage1_outcomes,
                         'TYPE 1 TRANSFER in STAGE 2': stage2_outcomes,
                         'TYPE 1 ROUND EARNING': type1_earning,
                         'TYPE 2 ROUND EARNING': type2_earning}
        history_table = pd.DataFrame(history_table, index=groups_id)
        history_table.index.name = "PARTNERSHIP"
        history_table = history_table.to_html(index=False, justify="justify-all")
        data_dict['history_table'] = history_table
        ### END - history table ###

        ### history graph ###
        type1_average_scores = ['-']
        type2_average_scores = ['-']
        for t in range(1, player.subsession.round_number):
            type1_scores = []
            type2_scores = []
            for p in player.subsession.get_players():
                if p.id_in_group == 1:
                    type1_scores.append(p.in_round(t).score)
                if p.id_in_group == 2:
                    type2_scores.append(p.in_round(t).score)
            type1_average_scores.append(round(np.average(type1_scores), 2))
            type2_average_scores.append(round(np.average(type2_scores), 2))
        data_dict['type1_average_scores'] = (type1_average_scores)
        data_dict['type2_average_score'] = (type2_average_scores)
        ### END - history graph ###

        return data_dict

class Stage1_waitpage(WaitPage):
    def after_all_players_arrive(group: Group):
        compute_partnership_outcome(group)
        set_payoffs_stage1(group)

class Stage1_outcome_page(Page):

    def is_displayed(player: Player):
        if player.subsession.round_number == 1:
            return player.id_in_group == 1 or player.id_in_group == 2
        else:
            return player.group.get_player_by_id(1).in_previous_rounds()[-1].exclusion_marking == 0


    def vars_for_template(player: Player):
        data_dict = {'': ''}
        data_dict['now'] = player.subsession.round_number
        data_dict['yesterday'] = player.subsession.round_number - 1
        data_dict['score'] = round(player.score,2)
        data_dict['type'] = player.id_in_group
        data_dict['stage1_outcome'] = player.group.stage1_partnership
        data_dict['cum_score'] = round(player.cum_score,2)

        data_dict['stage1_type1_decision'] = player.group.field_maybe_none('stage1_type1_decision')
        data_dict['stage1_type2_decision'] = player.group.field_maybe_none('stage1_type2_decision')

        ### history table ###
        groups_id = []
        stage1_outcomes = []
        stage2_outcomes = []
        type1_earning = []
        type2_earning = []
        for p in player.subsession.get_players():
            if p.id_in_group == 1:
                groups_id.append(p.group.id_in_subsession)
                if player.subsession.round_number == 1:
                    stage1_outcomes.append(' - ')
                    stage2_outcomes.append(' - ')
                    type1_earning.append(' - ')
                    type2_earning.append(' - ')
                else:
                    if p.in_previous_rounds()[-1].group.stage1_partnership == 1:
                        stage1_outcomes.append('YES')
                        if p.in_previous_rounds()[-1].group.stage2_delivery == 1:
                            stage2_outcomes.append('YES')
                            type1_earning.append(C.TYPE1_ENDOWMENT-C.TYPE1_ENDOWMENT+C.UTILITY_PARAMETER*(C.TYPE2_ENDOWMENT)**(1/2))
                            type2_earning.append(C.TYPE2_ENDOWMENT-C.TYPE2_ENDOWMENT+C.RHO*C.UTILITY_PARAMETER*(C.TYPE1_ENDOWMENT)**(1/2))
                        else:
                            stage2_outcomes.append('NO')
                            type1_earning.append(C.TYPE1_ENDOWMENT - C.TYPE1_ENDOWMENT + 2 * (C.TYPE2_ENDOWMENT) ** (1 / 2)+C.LAMBDA*C.RHO*C.TYPE2_ENDOWMENT)
                            type2_earning.append(C.TYPE2_ENDOWMENT - C.TYPE2_ENDOWMENT)
                    else:
                        stage1_outcomes.append('NO')
                        stage2_outcomes.append(' - ')
                        type1_earning.append(C.TYPE1_ENDOWMENT)
                        type2_earning.append(C.TYPE2_ENDOWMENT)
        groups_id = np.sort(groups_id)
        history_table = {'PARTNERSHIP': groups_id,
                         'TRADE AGREEMENT in STAGE 1': stage1_outcomes,
                         'TYPE 1 TRANSFER in STAGE 2': stage2_outcomes,
                         'TYPE 1 ROUND EARNING': type1_earning,
                         'TYPE 2 ROUND EARNING': type2_earning}
        history_table = pd.DataFrame(history_table, index=groups_id)
        history_table.index.name = "PARTNERSHIP"
        history_table = history_table.to_html(index=False, justify="justify-all")
        data_dict['history_table'] = history_table
        ### END - history table ###

        ### history graph ###
        type1_average_scores = ['-']
        type2_average_scores = ['-']
        for t in range(1, player.subsession.round_number):
            type1_scores = []
            type2_scores = []
            for p in player.subsession.get_players():
                if p.id_in_group == 1:
                    type1_scores.append(p.in_round(t).score)
                if p.id_in_group == 2:
                    type2_scores.append(p.in_round(t).score)
            type1_average_scores.append(round(np.average(type1_scores), 2))
            type2_average_scores.append(round(np.average(type2_scores), 2))
        data_dict['type1_average_scores'] = (type1_average_scores)
        data_dict['type2_average_score'] = (type2_average_scores)
        ### END - history graph ###

        return data_dict

class Stage2_type1_page(Page):

    form_model = 'group'
    form_fields = ['stage2_type1_decision']

    @staticmethod
    def is_displayed(player: Player):
        if player.subsession.round_number == 1:
            return player.id_in_group == 1 and player.group.stage1_partnership == 1
        else:
            return player.id_in_group == 1 and player.group.stage1_partnership == 1 and player.in_previous_rounds()[-1].exclusion_marking == 0

    def vars_for_template(player: Player):
        data_dict = {'': ''}
        data_dict['now'] = player.subsession.round_number
        data_dict['yesterday'] = player.subsession.round_number - 1
        data_dict['score'] = round(player.score,2)
        data_dict['cum_score'] = round(player.cum_score,2)
        data_dict['type'] = player.id_in_group
        data_dict['stage1_outcome'] = player.group.stage1_partnership
        data_dict['investment_outcome'] = C.RHO*C.TYPE1_ENDOWMENT
        data_dict['reneging_benefit'] = (C.LAMBDA*C.RHO*C.TYPE1_ENDOWMENT)*C.SCORE_SCALE

        ### history table ###
        groups_id = []
        stage1_outcomes = []
        stage2_outcomes = []
        type1_earning = []
        type2_earning = []
        for p in player.subsession.get_players():
            if p.id_in_group == 1:
                groups_id.append(p.group.id_in_subsession)
                if player.subsession.round_number == 1:
                    stage1_outcomes.append(' - ')
                    stage2_outcomes.append(' - ')
                    type1_earning.append(' - ')
                    type2_earning.append(' - ')
                else:
                    if p.in_previous_rounds()[-1].group.stage1_partnership == 1:
                        stage1_outcomes.append('YES')
                        if p.in_previous_rounds()[-1].group.stage2_delivery == 1:
                            stage2_outcomes.append('YES')
                            type1_earning.append(C.TYPE1_ENDOWMENT-C.TYPE1_ENDOWMENT+C.UTILITY_PARAMETER*(C.TYPE2_ENDOWMENT)**(1/2))
                            type2_earning.append(C.TYPE2_ENDOWMENT-C.TYPE2_ENDOWMENT+C.RHO*C.UTILITY_PARAMETER*(C.TYPE1_ENDOWMENT)**(1/2))
                        else:
                            stage2_outcomes.append('NO')
                            type1_earning.append(C.TYPE1_ENDOWMENT - C.TYPE1_ENDOWMENT + 2 * (C.TYPE2_ENDOWMENT) ** (1 / 2)+C.LAMBDA*C.RHO*C.TYPE2_ENDOWMENT)
                            type2_earning.append(C.TYPE2_ENDOWMENT - C.TYPE2_ENDOWMENT)
                    else:
                        stage1_outcomes.append('NO')
                        stage2_outcomes.append(' - ')
                        type1_earning.append(C.TYPE1_ENDOWMENT)
                        type2_earning.append(C.TYPE2_ENDOWMENT)
        groups_id = np.sort(groups_id)
        history_table = {'PARTNERSHIP': groups_id,
                         'TRADE AGREEMENT in STAGE 1': stage1_outcomes,
                         'TYPE 1 TRANSFER in STAGE 2': stage2_outcomes,
                         'TYPE 1 ROUND EARNING': type1_earning,
                         'TYPE 2 ROUND EARNING': type2_earning}
        history_table = pd.DataFrame(history_table, index=groups_id)
        history_table.index.name = "PARTNERSHIP"
        history_table = history_table.to_html(index=False, justify="justify-all")
        data_dict['history_table'] = history_table
        ### END - history table ###

        ### history graph ###
        type1_average_scores = ['-']
        type2_average_scores = ['-']
        for t in range(1, player.subsession.round_number):
            type1_scores = []
            type2_scores = []
            for p in player.subsession.get_players():
                if p.id_in_group == 1:
                    type1_scores.append(p.in_round(t).score)
                if p.id_in_group == 2:
                    type2_scores.append(p.in_round(t).score)
            type1_average_scores.append(round(np.average(type1_scores), 2))
            type2_average_scores.append(round(np.average(type2_scores), 2))
        data_dict['type1_average_scores'] = (type1_average_scores)
        data_dict['type2_average_score'] = (type2_average_scores)
        ### END - history graph ###



        return data_dict

class Stage2_waitpage(WaitPage):
    def after_all_players_arrive(group: Group):
        compute_delivery_outcome(group)
        set_payoffs_stage2(group)

        p1 = group.get_player_by_id(1)
        if group.stage2_type1_decision == 0:
            p1.exclusion_marking = 1


class Round_outcome_page(Page):
    def vars_for_template(player: Player):
        data_dict = {'': ''}
        data_dict['now'] = player.subsession.round_number
        data_dict['yesterday'] = player.subsession.round_number - 1
        data_dict['score'] = round(player.score,2)
        data_dict['cum_score'] = round(player.cum_score,2)
        data_dict['type'] = player.id_in_group
        data_dict['stage1_outcome'] = player.group.stage1_partnership
        data_dict['stage2_delivery'] = player.group.stage2_delivery
        data_dict['roll'] = C.ROUND_TERMINATION_ROLLS[player.subsession.round_number]

        data_dict['partner_score_type1'] = round(player.group.get_player_by_id(1).score, 2)
        data_dict['partner_score_type2'] = round(player.group.get_player_by_id(2).score, 2)

        if player.subsession.round_number == 1:
            data_dict['exclusion'] = 0
        else:
            if player.group.get_player_by_id(1).in_previous_rounds()[-1].exclusion_marking == 1:
                data_dict['exclusion'] = 1
            else:
                data_dict['exclusion'] = 0

        ### history table ###
        groups_id = []
        stage1_outcomes = []
        stage2_outcomes = []
        type1_earning = []
        type2_earning = []
        for p in player.subsession.get_players():
            if p.id_in_group == 1:
                groups_id.append(p.group.id_in_subsession)
                if player.subsession.round_number == 1:
                    stage1_outcomes.append(' - ')
                    stage2_outcomes.append(' - ')
                    type1_earning.append(' - ')
                    type2_earning.append(' - ')
                else:
                    if p.in_previous_rounds()[-1].group.stage1_partnership == 1:
                        stage1_outcomes.append('YES')
                        if p.in_previous_rounds()[-1].group.stage2_delivery == 1:
                            stage2_outcomes.append('YES')
                            type1_earning.append(C.TYPE1_ENDOWMENT-C.TYPE1_ENDOWMENT+C.UTILITY_PARAMETER*(C.TYPE2_ENDOWMENT)**(1/2))
                            type2_earning.append(C.TYPE2_ENDOWMENT-C.TYPE2_ENDOWMENT+C.RHO*C.UTILITY_PARAMETER*(C.TYPE1_ENDOWMENT)**(1/2))
                        else:
                            stage2_outcomes.append('NO')
                            type1_earning.append(C.TYPE1_ENDOWMENT - C.TYPE1_ENDOWMENT + 2 * (C.TYPE2_ENDOWMENT) ** (1 / 2)+C.LAMBDA*C.RHO*C.TYPE2_ENDOWMENT)
                            type2_earning.append(C.TYPE2_ENDOWMENT - C.TYPE2_ENDOWMENT)
                    else:
                        stage1_outcomes.append('NO')
                        stage2_outcomes.append(' - ')
                        type1_earning.append(C.TYPE1_ENDOWMENT)
                        type2_earning.append(C.TYPE2_ENDOWMENT)
        groups_id = np.sort(groups_id)
        history_table = {'PARTNERSHIP': groups_id,
                         'TRADE AGREEMENT in STAGE 1': stage1_outcomes,
                         'TYPE 1 TRANSFER in STAGE 2': stage2_outcomes,
                         'TYPE 1 ROUND EARNING': type1_earning,
                         'TYPE 2 ROUND EARNING': type2_earning}
        history_table = pd.DataFrame(history_table, index=groups_id)
        history_table.index.name = "PARTNERSHIP"
        history_table = history_table.to_html(index=False, justify="justify-all")
        data_dict['history_table'] = history_table
        ### END - history table ###

        ### history graph ###
        type1_average_scores = ['-']
        type2_average_scores = ['-']
        for t in range(1, player.subsession.round_number):
            type1_scores = []
            type2_scores = []
            for p in player.subsession.get_players():
                if p.id_in_group == 1:
                    type1_scores.append(p.in_round(t).score)
                if p.id_in_group == 2:
                    type2_scores.append(p.in_round(t).score)
            type1_average_scores.append(round(np.average(type1_scores), 2))
            type2_average_scores.append(round(np.average(type2_scores), 2))
        data_dict['type1_average_scores'] = (type1_average_scores)
        data_dict['type2_average_score'] = (type2_average_scores)
        ### END - history graph ###

        return data_dict

class Round_waitpage(WaitPage):
    wait_for_all_groups  = True


class Exclusion_type1_page(Page):

    def is_displayed(player: Player):
        if player.subsession.round_number > 1:
            return player.id_in_group == 1 and player.in_previous_rounds()[-1].exclusion_marking == 1

    def vars_for_template(player: Player):
        data_dict = {'': ''}
        data_dict['exclusion_marking'] = player.in_previous_rounds()[-1].exclusion_marking
        data_dict['now'] = player.subsession.round_number
        data_dict['yesterday'] = player.subsession.round_number - 1
        data_dict['score'] = round(player.score, 2)
        data_dict['cum_score'] = round(player.cum_score, 2)
        data_dict['type'] = player.id_in_group
        data_dict['stage1_outcome'] = player.group.stage1_partnership
        data_dict['stage2_delivery'] = player.group.stage2_delivery
        data_dict['roll'] = C.ROUND_TERMINATION_ROLLS[player.subsession.round_number]

        ### history table ###
        groups_id = []
        stage1_outcomes = []
        stage2_outcomes = []
        type1_earning = []
        type2_earning = []
        for p in player.subsession.get_players():
            if p.id_in_group == 1:
                groups_id.append(p.group.id_in_subsession)
                if player.subsession.round_number == 1:
                    stage1_outcomes.append(' - ')
                    stage2_outcomes.append(' - ')
                    type1_earning.append(' - ')
                    type2_earning.append(' - ')
                else:
                    if p.in_previous_rounds()[-1].group.stage1_partnership == 1:
                        stage1_outcomes.append('YES')
                        if p.in_previous_rounds()[-1].group.stage2_delivery == 1:
                            stage2_outcomes.append('YES')
                            type1_earning.append(
                                C.TYPE1_ENDOWMENT - C.TYPE1_ENDOWMENT + 2 * (C.TYPE2_ENDOWMENT) ** (1 / 2))
                            type2_earning.append(
                                C.TYPE2_ENDOWMENT - C.TYPE2_ENDOWMENT + C.RHO * 2 * (C.TYPE1_ENDOWMENT) ** (1 / 2))
                        else:
                            stage2_outcomes.append('NO')
                            type1_earning.append(C.TYPE1_ENDOWMENT - C.TYPE1_ENDOWMENT + 2 * (C.TYPE2_ENDOWMENT) ** (
                                        1 / 2) + C.LAMBDA * C.RHO * C.TYPE2_ENDOWMENT)
                            type2_earning.append(C.TYPE2_ENDOWMENT - C.TYPE2_ENDOWMENT)
                    else:
                        stage1_outcomes.append('NO')
                        stage2_outcomes.append(' - ')
                        type1_earning.append(C.TYPE1_ENDOWMENT)
                        type2_earning.append(C.TYPE2_ENDOWMENT)
        groups_id = np.sort(groups_id)
        history_table = {'PARTNERSHIP': groups_id,
                         'TRADE AGREEMENT in STAGE 1': stage1_outcomes,
                         'TYPE 1 TRANSFER in STAGE 2': stage2_outcomes,
                         'TYPE 1 ROUND EARNING': type1_earning,
                         'TYPE 2 ROUND EARNING': type2_earning}
        history_table = pd.DataFrame(history_table, index=groups_id)
        history_table.index.name = "PARTNERSHIP"
        history_table = history_table.to_html(index=False, justify="justify-all")
        data_dict['history_table'] = history_table
        ### END - history table ###

        ### history graph ###
        type1_average_scores = ['-']
        type2_average_scores = ['-']
        for t in range(1, player.subsession.round_number):
            type1_scores = []
            type2_scores = []
            for p in player.subsession.get_players():
                if p.id_in_group == 1:
                    type1_scores.append(p.in_round(t).score)
                if p.id_in_group == 2:
                    type2_scores.append(p.in_round(t).score)
            type1_average_scores.append(round(np.average(type1_scores), 2))
            type2_average_scores.append(round(np.average(type2_scores), 2))
        data_dict['type1_average_scores'] = (type1_average_scores)
        data_dict['type2_average_score'] = (type2_average_scores)
        ### END - history graph ###

        return data_dict


class Exclusion_type2_page(Page):

    def is_displayed(player: Player):
        if player.subsession.round_number > 1:
            return player.id_in_group == 2 and player.group.get_player_by_id(1).in_previous_rounds()[-1].exclusion_marking == 1

    def vars_for_template(player: Player):
        data_dict = {'': ''}
        data_dict['exclusion_marking'] = player.in_previous_rounds()[-1].exclusion_marking
        data_dict['now'] = player.subsession.round_number
        data_dict['yesterday'] = player.subsession.round_number - 1
        data_dict['score'] = round(player.score, 2)
        data_dict['cum_score'] = round(player.cum_score, 2)
        data_dict['type'] = player.id_in_group
        data_dict['stage1_outcome'] = player.group.stage1_partnership
        data_dict['stage2_delivery'] = player.group.stage2_delivery
        data_dict['roll'] = C.ROUND_TERMINATION_ROLLS[player.subsession.round_number]

        ### history table ###
        groups_id = []
        stage1_outcomes = []
        stage2_outcomes = []
        type1_earning = []
        type2_earning = []
        for p in player.subsession.get_players():
            if p.id_in_group == 1:
                groups_id.append(p.group.id_in_subsession)
                if player.subsession.round_number == 1:
                    stage1_outcomes.append(' - ')
                    stage2_outcomes.append(' - ')
                    type1_earning.append(' - ')
                    type2_earning.append(' - ')
                else:
                    if p.in_previous_rounds()[-1].group.stage1_partnership == 1:
                        stage1_outcomes.append('YES')
                        if p.in_previous_rounds()[-1].group.stage2_delivery == 1:
                            stage2_outcomes.append('YES')
                            type1_earning.append(
                                C.TYPE1_ENDOWMENT - C.TYPE1_ENDOWMENT + 2 * (C.TYPE2_ENDOWMENT) ** (1 / 2))
                            type2_earning.append(
                                C.TYPE2_ENDOWMENT - C.TYPE2_ENDOWMENT + C.RHO * 2 * (C.TYPE1_ENDOWMENT) ** (1 / 2))
                        else:
                            stage2_outcomes.append('NO')
                            type1_earning.append(C.TYPE1_ENDOWMENT - C.TYPE1_ENDOWMENT + 2 * (C.TYPE2_ENDOWMENT) ** (
                                        1 / 2) + C.LAMBDA * C.RHO * C.TYPE2_ENDOWMENT)
                            type2_earning.append(C.TYPE2_ENDOWMENT - C.TYPE2_ENDOWMENT)
                    else:
                        stage1_outcomes.append('NO')
                        stage2_outcomes.append(' - ')
                        type1_earning.append(C.TYPE1_ENDOWMENT)
                        type2_earning.append(C.TYPE2_ENDOWMENT)
        groups_id = np.sort(groups_id)
        history_table = {'PARTNERSHIP': groups_id,
                         'TRADE AGREEMENT in STAGE 1': stage1_outcomes,
                         'TYPE 1 TRANSFER in STAGE 2': stage2_outcomes,
                         'TYPE 1 ROUND EARNING': type1_earning,
                         'TYPE 2 ROUND EARNING': type2_earning}
        history_table = pd.DataFrame(history_table, index=groups_id)
        history_table.index.name = "PARTNERSHIP"
        history_table = history_table.to_html(index=False, justify="justify-all")
        data_dict['history_table'] = history_table
        ### END - history table ###

        ### history graph ###
        type1_average_scores = ['-']
        type2_average_scores = ['-']
        for t in range(1, player.subsession.round_number):
            type1_scores = []
            type2_scores = []
            for p in player.subsession.get_players():
                if p.id_in_group == 1:
                    type1_scores.append(p.in_round(t).score)
                if p.id_in_group == 2:
                    type2_scores.append(p.in_round(t).score)
            type1_average_scores.append(round(np.average(type1_scores), 2))
            type2_average_scores.append(round(np.average(type2_scores), 2))
        data_dict['type1_average_scores'] = (type1_average_scores)
        data_dict['type2_average_score'] = (type2_average_scores)
        ### END - history graph ###

        return data_dict




class End(Page):
    @staticmethod
    def vars_for_template(player: Player):
        pass

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.round_number == C.NUM_ROUNDS

    def vars_for_template(player: Player):
        data_dict = {'': ''}
        data_dict['cum_score'] = round(player.cum_score,2)
        if round((round(player.cum_score, 2)/100)*C.EXCHANGE_RATE,2) >= 0:
            data_dict['payoff'] = round((round(player.cum_score, 2)/100)*C.EXCHANGE_RATE,2)
        else:
            data_dict['payoff'] = 0

        return data_dict






page_sequence = [
    Introduction,
    Quiz,
    Type_page,
    Intro_waitpage,
    Exclusion_type1_page,
    Exclusion_type2_page,
    Stage1_type1_page,
    Stage1_type2_page,
    Stage1_waitpage,
    Stage1_outcome_page,
    Stage2_type1_page,
    Stage2_waitpage,
    Round_outcome_page,
    Round_waitpage,
    End
]
