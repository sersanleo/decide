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
        return Response(out)

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
        return Response(out)

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

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        if t == 'EQUALITY':
            return self.equality(opts)

        return Response({})
