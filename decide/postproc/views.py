from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

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
        
    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
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

        return Response(out)
