def test_total_initialization(models):
    """
    ensure that the `total` is auto populated.
    """
    survey = models.Survey.objects.create(num_expected=10)
    assert survey.total > 1000000
    assert survey.num_expected == 10
    assert survey.num_collected == 0
    assert survey._tracker == '1'
    assert survey.uuid
