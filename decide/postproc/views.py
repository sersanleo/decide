from rest_framework.views import APIView
from rest_framework.response import Response
import math


class PostProcView(APIView):

    def largest_remainder(self, options, q, points):
        out = []
        e = []
        r = []

        for opt in options:
            ei = math.floor(opt['votes']/q)
            e.append(ei)
            r.append(opt['votes']-q*ei)

        k = points - sum(e)

        for x in range(k):
            grtst_rest_index = r.index(max(r))
            e[grtst_rest_index] = e[grtst_rest_index] + 1
            r[grtst_rest_index] = -1

        cont = 0
        for opt in options:
            out.append({
                **opt,
                'postproc': e[cont],
                })
            cont += 1

        out.sort(key=lambda x: (-x['postproc'], -x['votes']))
        return out

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return out

    def borda(self, options):
        out = []

        for opt in options:
            votes = 0
            options_number = len(options)
            for i in range(0, options_number):
                votes += opt['votes'][i]*(options_number-i)
            out.append({
                **opt,
                'postproc': votes,
            })

        out.sort(key=lambda x: -x['postproc'])
        return out

    def equality(self, options):
        out = []
        n_women = 0
        n_men = 0

        for opt in options:
            n_women += opt['votes_women']
            n_men += opt['votes_men']

        for opt in options:
            if n_women > n_men:
                votes = opt['votes_men'] + opt['votes_women']*(n_men/n_women)
            else:
                votes = opt['votes_women'] + opt['votes_men']*(n_women/n_men)
            
            out.append({
                **opt,
                'postproc': round(votes),
            })

        out.sort(key=lambda x: -x['postproc'])

        return out

    def droop(self, options, points):
        total_votes = 0

        for opt in options:
            total_votes += opt['votes']

        q = round(1 + total_votes/(points+1))

        return self.largest_remainder(options, q, points)

    def sainte_lague(self, options, points):
        out = []
        votes = []
        points_for_opt = []

        for i in range(0, len(options)):
            votes.append(options[i]['votes'])
            points_for_opt.append(0)

        for i in range(0, points):
            max_index = votes.index(max(votes))
            points_for_opt[max_index] += 1
            votes[max_index] = options[max_index]['votes'] / (2 * points_for_opt[max_index] + 1)

        for i in range(0, len(options)):
            out.append({
                **options[i],
                'postproc': points_for_opt[i],
            })

        out.sort(key=lambda x: (-x['postproc'], -x['votes']))
        return out

    def imperiali(self, options, points):
        total_votes = 0

        for opt in options:
            total_votes += opt['votes']

        q = round(total_votes/(points+2))

        return self.largest_remainder(options, q, points)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | BORDA | DROOP
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        
        * type: EQUALITY
        * options: [
            {
             option: str,
             number: int,
             votes_men: int,
             votes_women: int,
            }
           ]

        * type: DROOP
        * points: int
        * options: [
            {
             option: str,
             number: int,
             votes: int,
            }
           ]
        """

        out = []
        questions = request.data

        for q in questions:
            t = q['type']
            opts = q['options']
            if t == 'IDENTITY':
                out.append(self.identity(opts))
            if t == 'BORDA':
                out.append(self.borda(opts))
            if t == 'EQUALITY':
                out.append(self.equality(opts))
            if t == 'SAINTE_LAGUE':
                out.append(self.sainte_lague(opts, q['points']))
            if t == 'DROOP':
                out.append(self.droop(opts, q['points']))
            if t == 'IMPERIALI':
                out.append(self.imperiali(opts, q['points']))

        return Response(out)
